from django.urls import include, path
from rest_framework import routers
from .views import TemplatesAPIView, SlideImagesAPIView, TemplatesPaginationStandardView, TemplatesAPIDetail, LikesPartialUpdateView, DownloadsPartialUpdateView, TemplatesPaginationSmalldView

router = routers.DefaultRouter()
# router.register(r'templates', views.TemplatesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/templates/', TemplatesAPIView.as_view()),
    path('api/templates/<str:id>', TemplatesAPIDetail.as_view(), name='template_detail'),
    path('api/templates/standard-pagination/', TemplatesPaginationStandardView.as_view()),
    path('api/templates/small-pagination/', TemplatesPaginationSmalldView.as_view()),
    path('api/templates/update-likes/<str:id>/<int:trend>/<int:amount>', LikesPartialUpdateView.as_view(), name='likes_partial_update'),
    path('api/templates/update-downloads/<str:id>/<int:amount>', DownloadsPartialUpdateView.as_view(), name='download_partial_update'),
    path('api/slideImages/', SlideImagesAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]