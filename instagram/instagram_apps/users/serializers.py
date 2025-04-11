from rest_framework import serializers 
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        if instance.profile_status == CustomUser.PRIVATE_PROFILE and not request.user.is_authenticated:
            return {
                'username': instance.username,
                'profile_picture': instance.profile_picture.url if instance.profile_picture else None,
                'message': 'This profile is private'
            }
          
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'profile_picture', 'bio')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user