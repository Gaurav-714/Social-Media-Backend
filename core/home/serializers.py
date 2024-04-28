from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Post


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
    class Meta:
        model = Post
        fields = "__all__"

        title = serializers.CharField()
        description = serializers.CharField()
        user = serializers.HiddenField(default=serializers.CurrentUserDefault())

        def update(self, instance, validated_data):
            if instance.user.id == validated_data['user']:
                return super().update(instance, validated_data)