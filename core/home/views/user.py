from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from home.serializers import UserSerializer, LoginSerializer
from home.models import User


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
                if user.password == serializer.validated_data['password']:
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
