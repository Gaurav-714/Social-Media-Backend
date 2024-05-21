from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from home.serializers import UserSerializer, LoginSerializer, FollowUserSerializer
from home.models import User, FollowUser


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class LoginView(APIView):
    def post(self, request): 
        try:
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                response = serializer.get_jwt_token(serializer.validated_data)
                return Response(response)
            else:
                return Response({
                'success' : False,
                'message' : 'Error occured.',
                'error' : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            print(ex)
            return Response({
                'success' : False,
                'message' : 'Something went wrong.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
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

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request):
        try:
            self.perform_destroy(request.user)
            return Response({
                'success' : True,
                'message' : 'Account deleted successfully.'
            }, status.HTTP_200_OK)      
    
        except Exception as ex:
            return Response({
                'success' : False,
                'message' : 'Error occured.',
                'error': str(ex)
            }, status.HTTP_400_BAD_REQUEST)



class FollowingUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = FollowUserSerializer

    def get(self, request, pk):
        try:
            user = User.objects.filter(id=pk)

            if not user.exists():
                return Response({
                    'success' : False,
                    'message' : 'User does not exists.'
                }, status = status.HTTP_404_NOT_FOUND)
            
            followed_by = FollowUser.objects.filter(followed_by=pk)
            following_to = FollowUser.objects.filter(following_to=pk)

            follower_serializer = self.serializer_class(followed_by, many=True)
            following_serializer = self.serializer_class(following_to, many=True)

            followers = []
            data = following_serializer.data
            for item in data:
                obj = item['followed_by']
                user = User.objects.get(id=obj)
                followers.append(user.username)

            following = []
            data = follower_serializer.data
            for item in data:
                obj = item['following_to']
                user = User.objects.get(id=obj)
                following.append(user.username)

            return Response({
                'success' : True,
                'followers_count' : len(followers),
                'followers' : followers,
                'following_count' : len(following),
                'following' : following
            })
        
        except Exception as ex:
            return Response({
                'success' : False,
                'message' : 'Error occured.',
                'error' : str(ex)
            })

    def post(self, request, pk):
        try:
            following_to = User.objects.get(id=pk)
            followed_by = FollowUser.objects.get_or_create(followed_by=request.user, following_to=following_to)

            if followed_by[1]:
                return Response({
                    'success' : True,
                    'message' : f'You followed {following_to.username}.'
                }, status=status.HTTP_200_OK)
            
            else:
                followed_by[0].delete()
                return Response({
                    'success' : True,
                    'message' : f'You unfollowed {following_to.username}.'
                }, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'User does not exists.' 
            }, status=status.HTTP_404_NOT_FOUND)