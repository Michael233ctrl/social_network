import datetime
from django.db.models import Q
from django.utils.timezone import make_aware
from rest_framework import viewsets, generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, LikeSerializer
from .models import Post, PostLike


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'], permission_classes=(IsAuthenticated, ))
    def like(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, many=False)
        if PostLike.objects.filter(post=post, user=request.user):
            return Response({'response': 'You already liked the post.'}, status=status.HTTP_400_BAD_REQUEST)
        PostLike.objects.create(post=post, user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=(IsAuthenticated, ))
    def unlike(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, many=False)
        if PostLike.objects.filter(post=post, user=request.user):
            like = PostLike.objects.get(post=post, user=request.user)
            like.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'response': 'You should like before unlike.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def likes(self, request, pk=None):
        post_likes = LikesListView.as_view()
        resp = post_likes(request._request, pk=pk)
        return resp


class LikesListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return PostLike.objects.filter(post=post)


class FilterLikes(views.APIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            queryset = PostLike.objects.filter(
                Q(liked_at__date__gte=make_aware(datetime.datetime.strptime(self.kwargs.get('start_date'), "%Y-%m-%d")))
                &
                Q(liked_at__date__lte=make_aware(datetime.datetime.strptime(self.kwargs.get('end_date'), "%Y-%m-%d")))
            )
        except ValueError:
            return Response({'response': 'Provide a valid date format.'}, status=status.HTTP_400_BAD_REQUEST)
        ser = LikeSerializer(queryset, many=True)
        return Response({'Likes in this period': len(ser.data)})
