from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from home.serializers import UserSerializer, LoginSerializer, FollowUserSerializer
from home.models import User, FollowUser


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email = serializer.validated_data['email'])
                username = serializer.validated_data['email']
                password = serializer.validated_data['password']
                authenticated = authenticate(username=username, password=password)
                if authenticated:
                    token, created = Token.objects.get_or_create(user = user)
                    return Response({
                        'success' : True,
                        'message' :'Logged in successfully.',
                        'token' : token.key,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'success' : False,
                        'message' : 'Incorrect email or password.'
                        }, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({
                    'success' : False,
                    'message' : 'User does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success' : False,
            'message' : 'Something went wrong.',
            'error' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully.'
            }, status=status.HTTP_200_OK)  
        else:
            return Response({
                'success': False,
                'message': 'Error while updating user.',

                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk):
        try:
            user = User.objects.get(id = pk)
            if user.id == request.user.id:
                self.perform_destroy(request.user)
                return Response({
                    'success' : True,
                    'message' : 'Account deleted successfully.'
                }, status.HTTP_200_OK)      
            else:
                return Response({
                    'success' : False,
                    'message' : 'Not enough permissions.'
                }, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS) 
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'User does not exists.'
            }, status.HTTP_404_NOT_FOUND)



class FollowingUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = FollowUserSerializer

    def get(self, request, pk):
        followed_by = FollowUser.objects.filter(followed_by=request.user)
        following_to = FollowUser.objects.filter(following_to=pk)

        follower_serializer = self.serializer_class(followed_by, many=True)
        following_serializer = self.serializer_class(following_to, many=True)

        return Response({
            'success' : True,
            'followers' : following_serializer.data,
            'following' : follower_serializer.data 
        })

    def post(self, request, pk):
        try:
            following_to = User.objects.get(id=pk)
            followed_by = FollowUser.objects.get_or_create(followed_by=request.user, following_to=following_to)
            if followed_by[1]:
                return Response({
                    'success' : True,
                    'message' : f'You followed {following_to}.'
                }, status=status.HTTP_200_OK)
            else:
                followed_by[0].delete()
                return Response({
                    'success' : True,
                    'message' : f'You unfollowed {following_to}.'
                }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'User does not exists.' 
            }, status=status.HTTP_404_NOT_FOUND)