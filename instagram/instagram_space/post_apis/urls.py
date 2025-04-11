from django.urls import path
from instagram_space.post_apis.views import *

app_name = 'post_apis'

urlpatterns = [
    path('posts/open/', OpenProfilePostListAPIView.as_view(), name='open_profile_posts'),
    path('posts/private/', PrivateProfilePostListAPIView.as_view(), name='private_profile_posts')
]