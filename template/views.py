from rest_framework import filters, generics, status
from .serializers import TemplatesSerializer, SlideImagesSerializer, StandardResultsSetPagination, SmallResultsSetPagination
from .models import Templates, SlideImages
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

class TemplatesAPIView(generics.ListCreateAPIView):
    search_fields = ['name', 'keywordsSearch', 'colors', 'styles', 'topics']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ['downloaded', 'likes']
    queryset= Templates.objects.all()
    serializer_class = TemplatesSerializer

class TemplatesAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplatesSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Templates.objects.filter(id=self.kwargs['id'])   

class SlideImagesAPIView(generics.ListCreateAPIView):
    serializer_class = SlideImagesSerializer
    queryset= SlideImages.objects.all()

class TemplatesPaginationStandardView(generics.ListCreateAPIView):
    search_fields = ['name', 'keywordsSearch', 'colors', 'styles', 'topics', 'authorUID']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ['downloaded', 'likes', 'create_at']
    queryset= Templates.objects.all()
    serializer_class = TemplatesSerializer
    pagination_class = StandardResultsSetPagination

class TemplatesPaginationSmalldView(generics.ListCreateAPIView):
    search_fields = ['name', 'keywordsSearch', 'colors', 'styles', 'topics', 'authorUID']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ['downloaded', 'likes', 'create_at']
    queryset= Templates.objects.all()
    serializer_class = TemplatesSerializer
    pagination_class = SmallResultsSetPagination

class LikesPartialUpdateView(APIView):

    def patch(self, request, id, trend, amount):
        # if no model exists by this PK, raise a 404 error
        model = get_object_or_404(Templates, pk=id)
        # this is the only field we want to update
        if trend==1:
            amount = amount
        else:
            amount = 0 - amount

        data = {"likes": model.likes + amount}
        serializer = TemplatesSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # return a meaningful error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadsPartialUpdateView(APIView):

    def patch(self, request, id, amount):
        # if no model exists by this PK, raise a 404 error
        model = get_object_or_404(Templates, pk=id)
        # this is the only field we want to update
        data = {"downloaded": model.downloaded + amount}
        serializer = TemplatesSerializer(model, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # return a meaningful error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)