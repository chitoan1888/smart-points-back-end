from django.contrib import admin
from .models import Templates, SlideImages

# Register your models here.
class SlideImagesAdmin(admin.StackedInline):
    model = SlideImages
@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    inline = [SlideImagesAdmin]
    list_display = ('name', 'colors', 'styles', 'topics', 'isPremium', 'likes', 'downloaded', 'create_at') 
    search_fields = ('name', 'keywordsSearch')
    list_filter = ('name', 'colors', 'styles', 'topics', 'isPremium')

@admin.register(SlideImages)
class SlideImagesAdmin(admin.ModelAdmin):
    list_display = ('slide_images', 'template')