from django.utils.html import strip_tags
from rest_framework import serializers

from .models import ActionItem, Entry


class EntryListSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    action_count = serializers.IntegerField(read_only=True)
    open_action_count = serializers.IntegerField(read_only=True)
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = [
            "id",
            "course",
            "course_name",
            "title",
            "lecture_date",
            "captured_at",
            "summary_due_at",
            "summary_written_at",
            "action_count",
            "open_action_count",
            "snippet",
        ]
        read_only_fields = [
            "id",
            "course",
            "title",
            "lecture_date",
            "captured_at",
            "summary_due_at",
            "summary_written_at",
        ]

    def get_snippet(self, obj):
        return strip_tags(obj.body)[:120]


class EntryDetailSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Entry
        fields = [
            "id",
            "user",
            "course",
            "course_name",
            "title",
            "body",
            "lecture_date",
            "captured_at",
            "summary_due_at",
            "summary_text",
            "summary_written_at",
            "ai_summary",
            "ai_summary_generated_at",
            "ai_summary_hidden",
            "ai_summary_stale",
            "version",
            "client_updated_at",
            "is_deleted",
            "deleted_at",
            "pg_created_at",
            "pg_modified_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "version",
            "summary_due_at",
            "ai_summary",
            "ai_summary_generated_at",
            "ai_summary_stale",
            "pg_created_at",
            "pg_modified_at",
        ]

    def validate_course(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Not your course.")
        return value


class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = [
            "id",
            "user",
            "entry",
            "text",
            "due_date",
            "is_done",
            "done_at",
            "source",
            "snoozed_until",
            "client_updated_at",
            "is_deleted",
            "deleted_at",
            "pg_created_at",
            "pg_modified_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "source",
            "pg_created_at",
            "pg_modified_at",
        ]

    def validate_entry(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Not your course.")
        return value
