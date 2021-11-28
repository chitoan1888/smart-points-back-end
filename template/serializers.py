from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from .models import Templates, SlideImages

class TemplatesSerializer(serializers.HyperlinkedModelSerializer):
    slide_image = serializers.StringRelatedField(many=True)

    class Meta:
        model = Templates
        fields = ('id', 'name', 'authorUID', 'description', 'keywordsSearch', 'likes', 'downloaded', 'colors', 'styles', 'topics', 'templates_file', 'slide_image', 'isPremium', 'create_at')

class SlideImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SlideImages
        fields = ('template', 'slide_images')

    def to_representation(self, instance):
        self.fields['template'] =  TemplatesSerializer(read_only=True)
        return super(SlideImagesSerializer, self).to_representation(instance)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000