from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_init
from datetime import date, datetime, timedelta
# from establishment.models import establishment


# Create your models here.

class member(models.Model):
    MALE = 'Mr'
    FEMALE = 'Mrs'

    GENDER_CHOICES = ( (MALE, 'Male'), (FEMALE, 'Female'))

    ANNUAL   = 'N'
    FREE     = 'F'
    LIFETIME = 'L'
    MEMBERSHIP_CHOICES = ( (FREE, 'Free'), (ANNUAL, 'Annual'), (LIFETIME, 'Life Time') )

    User_Name            = models.ForeignKey(User, on_delete=models.CASCADE)
    memebership_code     = models.CharField(max_length = 6)
    Name                 = models.CharField(max_length = 16)
    membership_start     = models.DateField(auto_now=False)
    renewal_date         = models.DateField(auto_now=False)
    days_left_to_renewal = models.IntegerField(editable=False)
    memebership_type     = models.CharField(max_length = 1, choices = MEMBERSHIP_CHOICES, default= ANNUAL)
    active               = models.BooleanField(default = True)
    gender               = models.CharField(max_length = 4, choices = GENDER_CHOICES,default = MALE)
    birthDay             = models.DateField(auto_now=False, default = '1980-01-01')
    Age                  = models.IntegerField(editable=False)
    job_title            = models.CharField(max_length=32, blank=True, null = True)
    company              = models.CharField(max_length=32, blank=True, null = True)
    email                = models.EmailField(max_length= 128)
    email2               = models.EmailField(max_length= 128, blank = True, null = True)
    phone                = models.PositiveIntegerField  (blank=True)
    phone2               = models.PositiveIntegerField  (blank=True, null = True)
    fax                  = models.PositiveIntegerField  (blank=True, null = True)
    profile_image        = models.ImageField(upload_to = 'profiles', null = True, blank = True)
    uploaded_at          = models.DateTimeField(auto_now_add = True, null = True )
    notes                = models.TextField(null=True, blank=True)



    def __str__ (self):
        return self.Name


class SubMember(models.Model):
    MALE = 'Mr'
    FEMALE = 'Mrs'
    GENDER_CHOICES = ( (MALE, 'Male'), (FEMALE, 'Female'))

    CHILD        = 'C'
    SUN_DAUGHTER = 'SD'
    SPOUSE       = 'S'
    sub_membership_type = ( (CHILD, 'Child-Under 12'), (SUN_DAUGHTER, 'Sun/Daughter 12+' ), (SPOUSE, 'Spouse') )

    main_user           = models.ForeignKey(member, on_delete=models.CASCADE, null = True, blank = True)
    sub_membership_type = models.CharField(max_length = 2, choices = sub_membership_type, default= SPOUSE)
    name                = models.CharField(max_length = 16)
    gender              = models.CharField(max_length = 4, choices = GENDER_CHOICES,default = MALE)
    birthDay            = models.DateField(default = '2008-01-01')
    job_title           = models.CharField(max_length=32, blank=True, null = True)
    company             = models.CharField(max_length=32, blank=True, null = True)
    phone               = models.PositiveIntegerField  (blank=True,  null = True)
    email               = models.EmailField(max_length= 128,  null = True)
    profile_image       = models.ImageField(upload_to = 'profiles', null = True, blank = True)
    sub_member_active   = models.BooleanField(default = True)

    def __str__ (self):
        return self.name


class SingleParent(models.Model):
    pass


def member_pre_save(instance, sender, *args, **kwargs):
    today    = date.today()
    if instance.memebership_type == 'N':
        start     = instance.membership_start
        end       = instance.renewal_date
        days_left = (end-today).days
        instance.days_left_to_renewal = days_left
    else:
        instance.renewal_date = today + timedelta(days=10000)
        instance.days_left_to_renewal = 10000

    instance.Age = today.year - instance.birthDay.year

pre_save.connect(member_pre_save, sender = member)


def count_days_post_init(instance, sender, *args, **kwargs):
    today    = date.today()
    if instance.id :

        if instance.memebership_type == 'N':
            start     = instance.membership_start
            end       = instance.renewal_date
            days_left = (end-today).days
            instance.days_left_to_renewal = days_left
        else:
            instance.days_left_to_renewal = 10000

        if instance.days_left_to_renewal <= -7:
            instance.active = False

post_init.connect(count_days_post_init, sender=member)
#
# def SubMemberPreSave(instance, sender,*args, **kwargs):
#
#     today = date.today()
#     if instance.sub_membership_type ==  'C':
#         if (today - instance.birthDay).days >= 4380:
#             raise ValueError ('The age is over 12 years!')
# pre_save.connect(SubMemberPreSave,sender=SubMember)
