from django.urls import path
from .views.user import CreateUser

urlpatterns = [
    path('user/create', CreateUser.as_view())
]
