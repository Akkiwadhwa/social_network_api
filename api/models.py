from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import Permission

class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])  # Add email validator
    password = models.CharField(max_length=128)  # Add password field
    geolocation = models.CharField(max_length=255, blank=True, null=True)
    is_holiday = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='api_user_set'  # Add a related_name argument to avoid clashes
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='api_user_set'  # Add a related_name argument to avoid clashes
    )

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title




