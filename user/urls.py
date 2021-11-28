from .views import *
from knox import views as knox_views
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),   
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/useruid/', UserAPI.as_view(), name='useruid'),
    path('api/userdata/', UserDataAPI.as_view(), name='userdata'),
    path('api/userdata/<str:uid>', UserDataAPIDetail.as_view(), name='userdatadetail'),
    path('api/userdata/update-premium/<str:uid>/<int:isPremium>', isPremiumPartialUpdateView.as_view(), name='isPremium_partial_update'),
    path('api/userdata/update-liked/<str:uid>/<str:action>/<str:idOrIndex>', TemplateLikedPartialUpdateView.as_view(), name='liked_partial_update'),
    path('api/userdata/update-downloaded/<str:uid>/<str:id>', TemplateDownloadedPartialUpdateView.as_view(), name='downloaded_partial_update'),
]