from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from home.models import Post, User, PostLike, PostComment
from home.serializers import PostSerializer, PostLikeSerializer, PostCommentSerializer

class CreatePost(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    
class RetrievePost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class UpdatePost(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)

            if post.user != request.user:
                return Response({
                    'success' : False,
                    'message' : 'You are not authorized for this.',
                }, status.HTTP_401_UNAUTHORIZED)
             
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
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)


class DeletePost(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            if post.user == request.user:
                self.perform_destroy(post)
                return Response({
                    'success' : True,
                    'message' : 'Post deleted successfully'
                }, status.HTTP_200_OK)
            else:
                return Response({
                    'success' : False,
                    'message' : 'You are not authorized for this.'
                }, status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)
        

class RetrieveUserPosts(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            user_posts = Post.objects.filter(user=pk)
            serializer = self.serializer_class(user_posts, many=True)
            return Response({
                'success' : True,
                'message' : f'Posts by {user.username}',
                'posts' : serializer.data
            })
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'User does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)


class LikePost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            likes = PostLike.objects.filter(post=post)
            serializer = PostLikeSerializer(likes, many=True)

            liked_users = []
            for data in serializer.data:
                user_id = data['user']
                user = User.objects.get(id=user_id)
                liked_users.append(user.username)

            return Response({
                'success' : True,
                'likes' : len(liked_users),
                'users' : liked_users
            }, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            new_like = PostLike.objects.get_or_create(user=request.user, post=post)

            if new_like[1]:
                return Response({
                    'message' : 'Post Liked.'
                }, status=status.HTTP_200_OK)
            else:
                new_like[0].delete()
                return Response({
                    'message' : 'Post Unliked.'
                }, status=status.HTTP_200_OK)
            
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.'
            }, status=status.HTTP_404_NOT_FOUND)
        

class CommentPost(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comments = PostComment.objects.filter(post=post)
        serializer = self.serializer_class(comments, many=True)

        data = serializer.data
        for item in data:
            obj = item['user']
            user = User.objects.get(id=obj)
            item['user'] = user.username

        if len(serializer.data) == 0:
            return Response({
                'success' : False,
                'message' : 'No comments found on this post.',
                'comments' : serializer.data
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'success' : True,
            'message' : 'Comments fetched successfully.',
            'count' : len(serializer.data),
            'comments' : serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = PostCommentSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save(post=post)

                return Response({
                    'success' : True,
                    'message' : 'Comment posted successfully.',
                    'data' : serializer.data
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'success' : False,
                     'message' : 'Error while posting comment.',
                     'error' : serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except ObjectDoesNotExist:
            return Response({
                'success' : False,
                'message' : 'Post does not exists.' 
            }, status=status.HTTP_404_NOT_FOUND)
        