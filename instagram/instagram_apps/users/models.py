from django.db import models
from django.contrib.auth.models import AbstractUser

 
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=155, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile/pictures', null=True, blank=True)

    @property
    def followers_count(self):
        return self.followers.count() 
    
    @property
    def followings_count(self):
        return self.followings.count()

    def __str__(self):
        return self.username