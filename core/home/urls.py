from django.urls import path
from .views.user import *
from .views.post import *

urlpatterns = [
    path('user/create', CreateUser.as_view()),
    path('user/login', LoginView.as_view()),
    path('user/<int:pk>', RetrieveUser.as_view()),
    path('user/update', UpdateUser.as_view()),
    path('user/delete/<int:pk>', DeleteUser.as_view()),

    path('post/create', CreatePost.as_view()),
    path('post/<int:pk>', RetrievePost.as_view()),
    path('post/update/<int:pk>', UpdatePost.as_view()),
    path('post/delete/<int:pk>', DeletePost.as_view()),
    path('posts', RetrieveUserPosts.as_view()),
    path('post/like/<int:pk>', LikeOnPost.as_view()),
]
