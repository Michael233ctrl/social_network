from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import RegisterAPIView, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
] + router.urls
