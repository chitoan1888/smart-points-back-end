from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import datetime
import uuid

def create_imgs_directory(self, filename):
        dirname = self.uid
        return "userProfilePics/{}/{}".format(dirname, filename)

class CustomUser(AbstractUser):
    uid = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs    )
        if not (UserInfo.objects.filter(uid=self.uid).first()):
            userInfo = UserInfo.objects.create(uid=self.uid)
            userInfo.save()   

class UserInfo(models.Model):
    uid = models.CharField(primary_key=True, max_length=100, unique=True, editable=False)
    displayName = models.CharField(max_length=100, default='')
    email = models.EmailField()
    profilePic = models.ImageField(upload_to=create_imgs_directory, null=True)
    phone = models.CharField(max_length=11, default='')
    GENDER_CHOICES = (
        ('M', 'Nam'),
        ('F', 'Nữ')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    dateOfBirth = models.DateField(default=datetime.date.today, blank=True)
    isPremium = models.BooleanField(default=False)
    templateLiked = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    templateDownloaded = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )