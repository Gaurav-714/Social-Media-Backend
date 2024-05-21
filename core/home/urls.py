from django.urls import path
from home.views.user import *
from home.views.post import *

urlpatterns = [
    path('user/create', CreateUser.as_view()),
    path('user/login', LoginView.as_view()),
    path('user/<int:pk>', RetrieveUser.as_view()),
    path('user/update', UpdateUser.as_view()),
    path('user/delete', DeleteUser.as_view()),
    path('user/follow/<int:pk>', FollowingUser.as_view()),

    path('post/create', CreatePost.as_view()),
    path('post/<int:pk>', RetrievePost.as_view()),
    path('post/update/<int:pk>', UpdatePost.as_view()),
    path('post/delete/<int:pk>', DeletePost.as_view()),
    path('posts/<int:pk>', RetrieveUserPosts.as_view()),
    path('post/like/<int:pk>', LikePost.as_view()),
    path('post/comment/<int:pk>', CommentPost.as_view()),
]
