from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=155, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile/pictures', null=True, blank=True)

    def __str__(self):
        return self.username