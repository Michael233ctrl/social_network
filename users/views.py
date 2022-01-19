from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from posts.permissions import IsAuthorOrReadOnly
from .serializers import RegisterSerializer, UserSerializer


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User created successfully.'
        })


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)
