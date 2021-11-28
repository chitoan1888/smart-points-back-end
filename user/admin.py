from django.contrib import admin
from .models import UserInfo,CustomUser

# Register your models here.
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('displayName', 'email', 'phone', 'gender', 'dateOfBirth', 'isPremium') 
    search_fields = ('displayName', 'email')
    list_filter = ('gender', 'isPremium')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'uid') 
    search_fields = ('username', 'email', 'uid')
