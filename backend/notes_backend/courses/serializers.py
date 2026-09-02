from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    entry_count = serializers.IntegerField(read_only=True)
    summarised_count = serializers.IntegerField(read_only=True)
    open_action_count = serializers.IntegerField(read_only=True)
    latest_entry_title = serializers.CharField(read_only=True)
    latest_entry_date = serializers.DateField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "user",
            "name",
            "is_archived",
            "entry_count",
            "summarised_count",
            "open_action_count",
            "latest_entry_title",
            "latest_entry_date",
            "client_updated_at",
            "is_deleted",
            "deleted_at",
            "pg_created_at",
            "pg_modified_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "pg_created_at",
            "pg_modified_at",
        ]
