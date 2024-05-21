from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from .models import User, Post, PostLike, PostComment


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):

        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is already taken.')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username is already taken.')
        
        return data

    def create(self, validated_data):

        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)

        validated_data['password'] = make_password(validated_data.get('password'))
        user =  User.objects.create(**validated_data)

        if groups_data:
            user.groups.set(groups_data)

        if user_permissions_data:
            user.user_permissions.set(user_permissions_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data.get('email', ''))
        if not user.exists():
            raise serializers.ValidationError('Account not found.')
        return data

    def get_jwt_token(self, validated_data):
        try:
            email = validated_data['email']
            password = validated_data['password']
            print(email, password)
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            print(user)
            if user:
                refresh = RefreshToken.for_user(user)
                return {
                    'success' : True,
                    'message' : 'Logged in successfully.',
                    'data' : {
                        'token' : {
                            'refresh': str(refresh),
                            'access' : str(refresh.access_token)
                        }
                    }
                }
            else:
                return {
                    'success' : False,
                    'message' : 'Invalid Credentials.',
                    'data' : {}
                }
        except Exception as ex:
            return {
                'success': False,
                'message': 'Authentication Error.',
                'error': str(ex)
            }


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
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        self.post = kwargs['post']
        user = self.context['request'].user
        return super().save(user=user, **kwargs)
    

class FollowUserSerializer(serializers.Serializer):
    followed_by = serializers.PrimaryKeyRelatedField(read_only=True)
    following_to = serializers.PrimaryKeyRelatedField(read_only=True)