from rest_framework import routers
from .views import AlbumViewSet

router = routers.DefaultRouter()
router.register('album', AlbumViewSet)

urlpatterns = router.urls
