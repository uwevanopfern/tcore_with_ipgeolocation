from django.urls import path
from .views import (
    SignupUserView,
    PostListCreateView,
    PostDetailView,
    LikeView,
    UnlikeView,
    UserDataListView,
)


urlpatterns = [
    path("/signup/", SignupUserView.as_view()),
    path("/posts/", PostListCreateView.as_view()),
    path("/posts/<int:id>", PostDetailView.as_view()),
    path("/likes/", LikeView.as_view()),
    path("/unlike/<int:id>", UnlikeView.as_view()),
    path("/user/data/", UserDataListView.as_view()),
]
