from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Post, PostLike, PostComment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return User.objects.create(**validated_data)
   

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    description = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class PostLikeSerializer(serializers.Serializer):
    class Meta:
        model = PostLike
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"

    comment = serializers.CharField(required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        print("Validated Data:", validated_data)
        request = self.context.get('request')
        print("Request:", request)
        if request and hasattr(request, 'post'):
            validated_data['post'] = request.post
        print("Modified Validated Data:", validated_data)
        return super().create(validated_data)
    
    """def save(self, **kwargs):
        print(kwargs)
        self.post = kwargs['post']
        return super().save(**kwargs)"""
    

class FollowUserSerializer(serializers.Serializer):
    followed_by = serializers.PrimaryKeyRelatedField(read_only=True)
    following_to = serializers.PrimaryKeyRelatedField(read_only=True)