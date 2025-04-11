from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from instagram_apps.posts.models import Post
from instagram_apps.followers.models import Follow
from instagram_apps.users.models import CustomUser
from instagram_apps.posts.serializers import PostSerializer
from instagram_space.utils.cutsom_pagination import CustomPagination


class OpenProfilePostListAPIView(APIView):
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagination = self.pagination_class()
        posts = Post.objects.filter(
            profile_profile_status=CustomUser.OPEN_PROFILE).order_by('-created_at')
        
        if posts.exists():
            result_page = pagination.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are not posts'}, status=status.HTTP_404_NOT_FOUND)


class PrivateProfilePostListAPIView(APIView):
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagination = self.pagination_class()
        user = request.user
        posts = Post.objects.filter(
            status=CustomUser.PRIVATE_PROFILE).order_by('-created_at')
        posts = posts.filter(user__in=user.followers.all())

        if posts.exists():
            result_page = pagination.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'No posts available'}, status=status.HTTP_404_NOT_FOUND)



