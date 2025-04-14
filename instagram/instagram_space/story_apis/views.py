from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import models

from instagram_apps.stories.models import Story
from instagram_apps.users.models import CustomUser
from instagram_apps.stories.serializers import StorySerializer
from instagram_space.utils.custom_pagination import CustomPagination
from instagram_space.utils.permissions import *



class OpenProfileStoryListAPIView(APIView):
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagination = self.pagination_class()
        stories = Story.visible_stories().filter(user__profile_status=CustomUser.OPEN_PROFILE, ).order_by('-created_at')
        
        if stories.exists():
            result_page = pagination.paginate_queryset(stories, request)
            serializer = StorySerializer(result_page, many=True, context={'request': request})
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are no stories'}, status=status.HTTP_200_OK)


class PrivateProfileStoryListAPIView(APIView):
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrOpenProfileOrFollowerPermission]

    def get(self, request):
        pagination = self.pagination_class()
        user = request.user
        stories = Story.visible_stories().filter(user__profile_status=CustomUser.PRIVATE_PROFILE).filter(
            models.Q(user__in=user.following.all()) | models.Q(user=user)
        ).order_by('-created_at')

        if stories.exists():
            result_page = pagination.paginate_queryset(stories, request)
            serializer = StorySerializer(result_page, many=True, context={'request': request})
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'No stories available'}, status=status.HTTP_200_OK)
    

class OpenProfileStoryDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story.visible_stories(), id=story_id)
    
        if story.user.profile_status == CustomUser.OPEN_PROFILE:
                serializer = StorySerializer(story, context={'request': request})
                return Response(serializer.data,  status=status.HTTP_200_OK)
        return Response({'message': 'This story is private'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        if request.user == story.user:
              story.delete()
              return Response({'message': 'Story deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        if request.user == story.user:
            serializer = StorySerializer(story, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Story updated successfully'}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)


class PrivateProfileStoryDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrOpenProfileOrFollowerPermission]

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story.visible_stories(), id=story_id)
       
        if story.user.profile_status == CustomUser.PRIVATE_PROFILE or story.user.id == request.user.id:
                serializer = StorySerializer(story, context={'request': request})
                return Response(serializer.data,  status=status.HTTP_200_OK)
        return Response({'message': 'This story is private'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        if request.user == story.user:
              story.delete()
              return Response({'message': 'Story deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, story_id):
        story = get_object_or_404(Story, id=story_id)
        if request.user == story.user:
            serializer = StorySerializer(story, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Story updated successfully'}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)


class CreateSingleStoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = StorySerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMultipleStoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = StorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)