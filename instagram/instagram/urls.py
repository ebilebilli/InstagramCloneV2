from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/v1/', include('apis.follower_apis.urls')),
    # path('api/v1/', include('apis.interaction_apis.urls')),
    path('api/v1/', include('instagram_space.post_apis.urls')),
    path('api/v1/', include('instagram_space.story_apis.urls')),
    # path('api/v1/',include('apis.user_apis.urls') ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)