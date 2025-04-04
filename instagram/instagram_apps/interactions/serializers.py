from rest_framework import serializers

from .models import Comment, Like
from instagram_apps.users.serializers import CustomUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__' 


class LikeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__' 