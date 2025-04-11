from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_status', 'bio', 'followers_count', 'followings_count', 'profile_picture')
    search_fields = ('username', 'email')
    list_filter = ('profile_status',)
    ordering = ('-date_joined',)
    list_per_page = 20

admin.site.register(CustomUser, CustomUserAdmin)
