from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from home.models import Post, User, PostLike
from home.serializers import PostSerializer

class CreatePost(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    
class RetrievePost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    
class UpdatePost(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'success' : True,
                'message' : 'Post updated successfully.'
            }, status.HTTP_200_OK)
        else:
            return Response({
                'success' : False,
                'message' : 'Error while updating post.',
                'error' : serializer.errors
            }, status.HTTP_400_BAD_REQUEST)


class DeletePost(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            if post.id == request.user.id:
                self.perform_destroy(post)
                return Response({
                    'success' : True,
                    'message' : 'Post deleted successfully'
                }, status.HTTP_200_OK)
            else:
                return Response({
                    'success' : False,
                    'message' : 'Not enough permissions.'
                }, status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
            
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)
        

class RetrieveUserPosts(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user_posts = Post.objects.filter(user=request.user.id)
        serializer = self.serializer_class(user_posts, many=True)
        return Response({
            'success' : True,
            'message' : f'Posts by : {user.username}',
            'posts' : serializer.data
        })


class LikeOnPost(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            new_like = PostLike.objects.get_or_create(user=request.user, post=post)
            if new_like[1]:
                return Response({
                    'success' : True,
                    'message' : 'Post Liked.'
                })
            else:
                new_like[0].delete()
                return Response({
                    'success' : True,
                    'message' : 'Post Unliked.'
                })
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.'
            })
        