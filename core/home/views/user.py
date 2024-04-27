from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from home.serializers import UserSerializer, LoginSerializer
from home.models import User


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email = serializer.validated_data['email'])
                if user.password == serializer.validated_data['password']:
                    token, created = Token.objects.get_or_create(user = user)
                    return Response({
                        'success' : True,
                        'token' : token.key
                    })
                else:
                    return Response({
                        'success' : False,
                        'message' :'incorrect email or password.'
                        })
                
            except ObjectDoesNotExist:
                return Response({
                    'success' : False,
                    'message' : 'user does not exist.'
            })
        return Response({
            'success' : False,
            'message' : 'something went wrong.'

        })