from django.urls import path
from instagram_space.story_apis.views import *

app_name = 'story_apis'

urlpatterns = [
    path('stories/open/', OpenProfileStoryListAPIView.as_view(), name='open-profile-stories'),
    path('stories/private/', PrivateProfileStoryListAPIView.as_view(), name='private-profile-stories'),
    path('story/detail/<int:post_id>/open/', OpenProfileStoryDetail.as_view(), name='open_story_detail'),
    path('story/detail/<int:post_id>/private/', PrivateProfileStoryDetail.as_view(), name='private_story_detail'),
    path('stories/create/single', CreateSingleStoryAPIView.as_view(), name='create-single-story'),
    path('stories/create/multiple', CreateMultipleStoriesAPIView.as_view(), name='create-multiple-stories'),
]