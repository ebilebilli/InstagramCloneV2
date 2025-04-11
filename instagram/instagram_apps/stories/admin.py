from django.contrib import admin
from .models import Story

class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'views', 'image', 'video')
    list_filter = ('created_at', 'user', 'views')
    search_fields = ('user__username', 'caption')
    ordering = ('-created_at',)
    list_per_page = 20

admin.site.register(Story, StoryAdmin)
