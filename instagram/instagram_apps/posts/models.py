from django.db import models
from django.core.exceptions import ValidationError

from instagram_apps.users.models import CustomUser



class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    caption = models.TextField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if not self.caption and not self.image and not self.video:
            raise ValidationError('You must choose at least one image,caption or video')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'