from rest_framework import serializers

from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, data):
        if data['follower'] == data['following']:
            raise serializers.ValidationError('You cannot fallow yourself')
        return data
