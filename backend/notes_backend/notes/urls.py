from rest_framework.routers import DefaultRouter
from .views import EntryViewSet, ActionItemViewSet

router = DefaultRouter()
router.register("entries", EntryViewSet, basename="entry")
router.register("action-items", ActionItemViewSet, basename="action-item")

urlpatterns = router.urls
