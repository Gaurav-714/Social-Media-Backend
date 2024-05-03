from django.db import models
from django.contrib.auth.models import AbstractUser
from home.manager import UserManager


class User(AbstractUser):
    username = None # Overrides the default username field provided by AbstractUser
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=150, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()


class Post(models.Model):
    image = models.ImageField(max_length=None)
    #title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class PostLike(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('user','post'), )


class PostComment(models.Model):
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)


class FollowUser(models.Model):
    followed_by = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='follower')
    following_to = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='following')