import uuid

from django.db import models

from django.conf import settings
from django.utils import timezone

# Create your models here.


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )

    # sync
    version = models.PositiveIntegerField(default=1)
    client_updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    pg_created_at = models.DateTimeField(auto_now_add=True)
    pg_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_course_per_user"
            )
        ]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
