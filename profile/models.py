from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save, post_init, post_delete, pre_delete
from members.models import member



# Create your models here.

class memberProfile(models.Model):

    member           = models.OneToOneField(member, on_delete=models.CASCADE)
    password         = models.CharField(max_length = 512)
    facebook         = models.URLField(verbose_name= 'Facebook', blank = True, null = True)
    twitter          = models.URLField(verbose_name= 'Twitter', blank = True, null = True)
    instagarm        = models.URLField(verbose_name= 'Instagram', blank = True, null = True)
    addetional_email = models.EmailField(blank = True, null = True)
    active           = models.BooleanField(default = False)


    def __str__(self):
        return "{} {}'s extended profile".format(self.member.first_name, self.member.last_name)

def memberprofile_pre_save(instance, sender, *args, **kwargs):
    user = User.objects.get(username= instance.member.User_Name)
    if instance._state.adding == True:
        instance.password = user.password
    user.set_password(instance.password)

pre_save.connect(memberprofile_pre_save, sender=memberProfile)

#
# class extendedProfile(AbstractBaseUser):
#
#     member           = models.OneToOneField(member, on_delete=models.CASCADE)
#     password         = models.CharField(max_length = 16)
#     facebook         = models.URLField(verbose_name= 'Facebook', blank = True, null = True)
#     twitter          = models.URLField(verbose_name= 'Twitter', blank = True, null = True)
#     instagarm        = models.URLField(verbose_name= 'Instagram', blank = True, null = True)
#     addetional_email = models.EmailField(blank = True, null = True)
#     active           = models.BooleanField(default = False)
#
#     REQUIRED_FIELDS = []
#     USERNAME_FIELD  = 'member'
#     def __str__(self):
#         return "{} {}'s profile".format(self.member.first_name, self.member.last_name)
