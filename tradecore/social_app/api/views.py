from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.contrib.auth.models import User
from social_app.models import Post, Like
from .serializers import (
    UserSerializer,
    PostSerializer,
    LikeSerializer,
)
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated


class SignupUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title", "user__username", "content")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"


class LikeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post = serializer.validated_data.get("post")
        if post:
            post.like_count = post.like_count + 1
            post.save()
        serializer.save(user=self.request.user, post=post)


class UnlikeView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "id"

    def perform_destroy(self, instance):
        post = instance.post
        if post.like_count > 0:
            post.like_count = post.like_count - 1
            post.save()
            instance.delete()


class UserDataListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
