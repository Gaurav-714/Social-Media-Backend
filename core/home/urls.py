from django.urls import path
from .views.user import *

urlpatterns = [
    path('user/create', CreateUser.as_view()),
    path('user/login', LoginView.as_view()),
    path('user/<int:pk>', RetriveUser.as_view()),
    path('user/update', UpdateUser.as_view()),
    path('user/delete/<int:pk>', DeleteUser.as_view())
]
