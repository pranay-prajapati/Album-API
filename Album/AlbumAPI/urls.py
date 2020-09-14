from rest_framework import routers
from .views import AlbumViewSet

router = routers.DefaultRouter()
router.register('album',AlbumViewSet)
#router.register('song',SongViewSet)

urlpatterns = router.urls