from django.urls import path
from instagram_space.post_apis.views import *

app_name = 'post_apis'

urlpatterns = [
    path('posts/open/', OpenProfilePostListAPIView.as_view(), name='open-profile-posts'),
    path('posts/private/', PrivateProfilePostListAPIView.as_view(), name='private-profile-posts'),
    path('post/detail/<int:post_id>/open/', OpenProfilePostDetail.as_view(), name='open_post_detail'),
    path('post/detail/<int:post_id>/private/', PrivateProfilePostDetail.as_view(), name='private_post_detail')
]