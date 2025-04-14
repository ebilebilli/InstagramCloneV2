from rest_framework import serializers 

from .models import Story
from instagram_apps.users.serializers import CustomUserSerializer

class StorySerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
  
    class Meta:
        model = Story
        fields = '__all__' 
    
    def get_image_url(self, object):
        if object.image:
            return object.image.url
        return None
    
    def get_video_url(self, object):
        if object.video:
            return object.video.url
        return None
    
    def get_is_expired(self, obj):
        return obj.is_expired()