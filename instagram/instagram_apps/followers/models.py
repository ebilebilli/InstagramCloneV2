from django.core.exceptions import ValidationError

from django.db import models
from instagram_apps.users.models import *

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='followings', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']
    
    def clean(self):
        if self.follower == self.following:
            raise ValidationError('You cannot fallow yourself')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'