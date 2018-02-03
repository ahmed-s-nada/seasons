from django.db import models
from django.contrib.auth.models import User
from members.models import member



# Create your models here.

class memberProfile(models.Model):

    member           = models.OneToOneField(member, on_delete=models.CASCADE)
    password         = models.CharField(max_length = 16)
    facebook         = models.URLField(verbose_name= 'Facebook', blank = True, null = True)
    twitter          = models.URLField(verbose_name= 'Twitter', blank = True, null = True)
    instagarm        = models.URLField(verbose_name= 'Instagram', blank = True, null = True)
    addetional_email = models.EmailField(blank = True, null = True)
    active           = models.BooleanField(default = False)


    def __str__(self):
        return "{} {}'s profile".format(self.member.first_name, self.member.last_name)
