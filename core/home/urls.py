from django.urls import path
from .views.user import CreateUser, LoginView

urlpatterns = [
    path('user/create', CreateUser.as_view()),
    path('user/login', LoginView.as_view())
]
