from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from home.models import Post
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