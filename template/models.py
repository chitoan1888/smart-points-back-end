from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.postgres.fields import ArrayField
import uuid
# Create your models here.

def create_directory(instance, filename):
    dirname = instance.id
    return "templates/{}/{}".format(dirname, filename)

def create_imgs_directory(instance, filename):
    dirname = instance.template.id
    return "templates/{}/imgs/{}".format(dirname, filename)
    
class Templates(models.Model):
    id = models.CharField(primary_key=True, max_length=100, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=None)
    authorUID = models.CharField(max_length=100)
    likes = models.IntegerField(default=0);
    downloaded = models.IntegerField(default=0);
    keywordsSearch = ArrayField(
        models.CharField(max_length=50),
    )
    isPremium = models.BooleanField(default=False)
    COLORS_CHOICES = (
        ('red', 'Đỏ'),
        ('orange', 'Cam'),
        ('yellow', 'Vàng'),
        ('blue', 'Xanh dương'),
        ('green', 'Xanh lá'),
        ('purple', 'Tím'),
        ('brown', 'Nâu'),
        ('white', 'Trắng'),
        ('black', 'Đen'),
    )
    colors = ArrayField(
        models.CharField(max_length=10, choices=COLORS_CHOICES, default='')
    )

    STYLES_CHOICES = (
        ('sport', 'Thể thao'),
        ('creative', 'Sáng tạo'),
        ('cute', 'Đáng yêu'),
        ('funny', 'Hài hước'),
        ('modern','Hiện đại'),
        ('simple','Đơn giản'),
        ('vintage','Hoài cổ'),
        ('elegant','Tao nhã'),
        ('cartoon', 'Hoạt hình'),
        ('minimalist', 'Tối giản'),
    )
    styles = ArrayField(
        models.CharField(max_length=20, choices=STYLES_CHOICES, default='')
    )

    TOPIC_CHOICES = (
        ('education', 'Giáo dục'),
        ('business', 'Kinh doanh'),
        ('marketing','Marketing'),
        ('medical','Y học'),
        ('multiPurpose','Đa mục đích'),
        ('infoGraphic','Sơ đồ'),
    )

    topics = ArrayField(
        models.CharField(max_length=20, choices=TOPIC_CHOICES, default='')
    )

    templates_file = models.FileField(upload_to=create_directory)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class SlideImages(models.Model):
    template = models.ForeignKey(Templates, related_name="slide_image", on_delete=models.CASCADE)
    slide_images = models.ImageField(upload_to=create_imgs_directory)

    def __str__(self):
        return self.slide_images.url