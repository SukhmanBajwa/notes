from django.db.models import Q
from django.db.models.aggregates import Count
from rest_framework import viewsets

from notes.models import ActionItem, Entry
from notes.serializers import (
    ActionItemSerializer,
    EntryDetailSerializer,
    EntryListSerializer,
)


class EntryViewSet(viewsets.ModelViewSet):

    # One view two serializers
    def get_serializer_class(self):
        if self.action == "list":
            return EntryListSerializer
        return EntryDetailSerializer

    def get_queryset(self):
        return (
            Entry.objects.filter(user=self.request.user, is_deleted=False)
            # only select data related to course
            .select_related("course")
            # make action count and open action count coloumns
            .annotate(
                action_count=Count(
                    "action_items", filter=Q(action_items__is_deleted=False)
                ),
                open_action_count=Count(
                    "action_items",
                    filter=Q(
                        action_items__is_done=False, action_items__is_deleted=False
                    ),
                ),
            )
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActionItemViewSet(viewsets.ModelViewSet):
    serializer_class = ActionItemSerializer

    # eager loading related data
    def get_queryset(self):
        return ActionItem.objects.filter(
            user=self.request.user, is_deleted=False
        ).select_related("entry", "entry__course")

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
