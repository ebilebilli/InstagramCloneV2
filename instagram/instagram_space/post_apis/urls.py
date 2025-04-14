from django.urls import path
from instagram_space.post_apis.views import *

app_name = 'post_apis'

urlpatterns = [
    path('posts/open/', OpenProfilePostListAPIView.as_view(), name='open-profile-posts'),
    path('posts/private/', PrivateProfilePostListAPIView.as_view(), name='private-profile-posts'),
    path('post/detail/<int:post_id>/open/', OpenProfilePostDetail.as_view(), name='open_post_detail'),
    path('post/detail/<int:post_id>/private/', PrivateProfilePostDetail.as_view(), name='private_post_detail'),
    path('posts/create/single', CreateSinglePostAPIView.as_view(), name='create-single-post'),
    path('posts/create/multiple', CreateMultiplePostsAPIView.as_view(), name='create-multiple-posts'),
]