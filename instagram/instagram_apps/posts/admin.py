from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'like_count', 'views', 'image', 'video')
    list_filter = ('created_at', 'user', 'like_count', 'views')
    search_fields = ('user__username', 'caption')
    ordering = ('-created_at',)
    list_per_page = 20

admin.site.register(Post, PostAdmin)
