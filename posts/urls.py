from django.urls import re_path
from rest_framework.routers import SimpleRouter
from .views import PostViewSet, FilterLikes

router = SimpleRouter()
router.register('', PostViewSet, basename='posts')


urlpatterns = [
    re_path('^analytics/date_from=(?P<start_date>.+)&date_to=(?P<end_date>.+)/$', FilterLikes.as_view())
] + router.urls
