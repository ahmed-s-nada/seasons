from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class userProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=None)
    favSite = models.URLField(blank = True)
    favPhoto = models.ImageField(upload_to = 'info_images', blank = True)

    def __str__(self):
        return self.user.username

    
