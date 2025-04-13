from rest_framework.permissions import BasePermission
from instagram_apps.users.models import CustomUser
from instagram_apps.followers.models import Follow


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrOpenProfileOrFollowerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        owner = obj.user

        if owner == user:
            return True

        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            if owner.profile_status == CustomUser.OPEN_PROFILE:
                return True

            is_follower = Follow.objects.filter(follower=user, following=owner).exists()
            if is_follower:
                return True

        return False
