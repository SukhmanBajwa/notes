import uuid

from django.db import models
from django.conf import settings
from courses.models import Course
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Source(models.TextChoices):
    USER = "user", "User"
    AI = "ai", "AI"


class Status(models.TextChoices):
    NEW = (
        "new",
        "New",
    )
    SAVED = (
        "saved",
        "Saved",
    )
    SKIPPED = (
        "skipped",
        "Skipped",
    )
    DUPLICATE = "duplicate", "Duplicate"


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entries"
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="entries")

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    lecture_date = models.DateField()

    # the 12-hour window
    captured_at = models.DateTimeField(default=timezone.now)
    summary_due_at = models.DateTimeField(null=True, blank=True)
    summary_text = models.TextField(blank=True)
    summary_written_at = models.DateTimeField(null=True, blank=True)

    # AI
    ai_summary = models.TextField(blank=True)
    ai_summary_generated_at = models.DateTimeField(null=True, blank=True)
    ai_summary_hidden = models.BooleanField(default=False)
    ai_summary_stale = models.BooleanField(default=False)

    # sync
    version = models.PositiveIntegerField(default=1)
    client_updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    pg_created_at = models.DateTimeField(auto_now_add=True)
    pg_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-lecture_date",
            "-captured_at",
        ]  # The minus prefix means descending.
        verbose_name_plural = "entries"  # overriding django defualt pluralization from "Entrys to entries"
        indexes = [
            models.Index(fields=["user", "-lecture_date"]),
            models.Index(fields=["user", "summary_due_at"]),
        ]

    def __str__(self):
        return f"{self.title}"

    # override save to calculate the due time for 12th hour user summary
    def save(self, *args, **kwargs):
        if self.captured_at and not self.summary_due_at:
            self.summary_due_at = self.captured_at + timedelta(hours=12)
        super().save(*args, **kwargs)


class ActionItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="action_items"
    )
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="action_items"
    )
    text = models.CharField(max_length=300)
    due_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(
        max_length=20, choices=Source.choices, default=Source.USER
    )
    snoozed_until = models.DateField(
        null=True,
        blank=True,
    )
    # sync
    version = models.PositiveIntegerField(default=1)
    client_updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    pg_created_at = models.DateTimeField(auto_now_add=True)
    pg_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"


class Suggestion(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="suggestions"
    )
    text = models.CharField(max_length=300)
    suggested_due = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    resolved_at = models.DateTimeField(null=True, blank=True)

    pg_created_at = models.DateTimeField(auto_now_add=True)
    pg_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pg_created_at"]

    def __str__(self):
        return f"{self.text}"
