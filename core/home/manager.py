from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if not kwargs["is_staff"]:
            raise ValueError("Superuser must have is_staff=True.")
        
        if not kwargs["is_superuser"]:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **kwargs)
        