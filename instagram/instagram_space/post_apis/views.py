from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import models

from instagram_apps.posts.models import Post
from instagram_apps.followers.models import Follow
from instagram_apps.users.models import CustomUser
from instagram_apps.posts.serializers import PostSerializer
from instagram.instagram_space.utils.custom_pagination import CustomPagination
from instagram_space.utils.permissions import *


class OpenProfilePostListAPIView(APIView):
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagination = self.pagination_class()
        posts = Post.objects.filter(
            user__profile_status=CustomUser.OPEN_PROFILE).order_by('-created_at')
        
        if posts.exists():
            result_page = pagination.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True, context={'request': request})
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are no posts'}, status=status.HTTP_200_OK)


class PrivateProfilePostListAPIView(APIView):
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrOpenProfileOrFollowerPermission]

    def get(self, request):
        pagination = self.pagination_class()
        user = request.user
        posts = Post.objects.filter(user__profile_status=CustomUser.PRIVATE_PROFILE).filter(
            models.Q(user__in=user.following.all()) | models.Q(user=user)
        ).order_by('-created_at')

        if posts.exists():
            result_page = pagination.paginate_queryset(posts, request)
            serializer = PostSerializer(result_page, many=True, context={'request': request})
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'No posts available'}, status=status.HTTP_200_OK)
    

class OpenProfilePostDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.user.profile_status == CustomUser.OPEN_PROFILE:
                serializer = PostSerializer(post, context={'request': request})
                return Response(serializer.data,  status=status.HTTP_200_OK)
        return Response({'message': 'This post is private'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
              post.delete()
              return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Post updated successfully'}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)


class PrivateProfilePostDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrOpenProfileOrFollowerPermission]

    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.user.profile_status == CustomUser.PRIVATE_PROFILE or post.user.id == request.user.id:
                serializer = PostSerializer(post, context={'request': request})
                return Response(serializer.data,  status=status.HTTP_200_OK)
        return Response({'message': 'This post is private'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
              post.delete()
              return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.user:
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Post updated successfully'}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)




