from rest_framework import generics
from home.serializers import UserSerializer
from home.models import User
#from django.contrib.auth.models import User

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer