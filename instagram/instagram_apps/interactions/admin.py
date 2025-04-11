from django.contrib import admin
from .models import Comment, Like

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'post', 'story')
    search_fields = ('user__username', 'text', 'post__caption', 'story__caption')
    list_filter = ('created_at', 'user', 'post', 'story')
    ordering = ('-created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'post', 'story', 'comment')
    search_fields = ('user__username', 'post__caption', 'story__caption', 'comment__text')
    list_filter = ('created_at', 'user', 'post', 'story', 'comment')
    ordering = ('-created_at',)

admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
