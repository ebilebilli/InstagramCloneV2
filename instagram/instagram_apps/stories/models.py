from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

from instagram_apps.users.models import CustomUser

class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    caption = models.TextField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='story_images/', null=True, blank=True)
    video = models.FileField(upload_to='story_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
    
    @staticmethod
    def visible_stories():
        time_limit = timezone.now() - timedelta(hours=24)
        return Story.visible_stories().objects.filter(created_at__gte=time_limit)

    def clean(self):
        caption = self.caption.strip() if self.caption else ''
        if not caption and not self.image and not self.video:
            raise ValidationError('You must choose at least one image,caption or video')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.caption[:20]}'
