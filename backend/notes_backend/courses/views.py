from django.db.models import Count, OuterRef, Q, Subquery
from rest_framework import viewsets

from notes.models import Entry

from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """List/create/retrieve/update/delete courses for the logged-in user.

    Each course comes back with the numbers its library card needs:
    entry count, how many of those have a summary (the progress bar),
    open action items, and the most recent lecture's title and date.
    """

    serializer_class = CourseSerializer

    def get_queryset(self):
        # A recipe, not a query yet: "this course's live entries, newest first."
        # OuterRef("pk") is a blank filled in with whichever course row the
        # outer query is currently on. Reused by both Subqueries below, so the
        # title and date always come from the same entry.
        latest = Entry.objects.filter(course=OuterRef("pk"), is_deleted=False).order_by(
            "-lecture_date", "-captured_at"
        )
        # Three annotations join the data
        # course  | entry           | e_del | e_summ | action           | a_done
        # --------+-----------------+-------+--------+------------------+-------
        # PSY 214 | Attention       | False |   0    | Skim Broadbent   | False
        # PSY 214 | DELETED LECTURE | True  |   1    | None             | None
        # PSY 214 | Working memory  | False |   1    | Re-read Baddeley | False
        # PSY 214 | Working memory  | False |   1    | Ask slide 22     | False
        # PSY 214 | Working memory  | False |   1    | Download slides  | True
        # CS 240  | Balanced trees  | False |   0    | AVL rotations    | False

        # annotate with make 3 new coloumns with new calculated information.
        return Course.objects.filter(user=self.request.user, is_deleted=False).annotate(
            # entry_count — rejects only DELETED LECTURE.
            # 4 rows pass, but they're just 2 distinct entries (Working memory ×3, Attention ×1).
            # Without distinct: 4. With: 2.
            entry_count=Count(
                "entries",
                filter=Q(entries__is_deleted=False),
                distinct=True,
            ),
            # summarised_count — additionally rejects Attention for having no summary.
            # 3 rows pass, all the same entry. Without distinct: 3. With: 1.
            summarised_count=Count(
                "entries",
                filter=Q(
                    entries__is_deleted=False,
                    entries__summary_written_at__isnull=False,
                ),
                distinct=True,
            ),
            # open_action_count — reads the action column instead.
            # Rejects "Download slides" as done. 3,
            # and distinct changes nothing,
            # because nothing joins below action items to repeat them.
            open_action_count=Count(
                "entries__action_items",
                filter=Q(
                    entries__action_items__is_done=False,
                    entries__action_items__is_deleted=False,
                ),
            ),
            latest_entry_title=Subquery(latest.values("title")[:1]),
            latest_entry_date=Subquery(latest.values("lecture_date")[:1]),
        )

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
