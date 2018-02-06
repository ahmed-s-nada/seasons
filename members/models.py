from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_init
from datetime import date, datetime, timedelta
# from .forms import member_form
from django.utils.text import slugify
from django.core.mail import send_mail
# from establishment.models import establishment


# Create your models here.

class member(models.Model):
    # form = MemberForm
    MALE = 'Mr'
    FEMALE = 'Mrs'

    GENDER_CHOICES = ( (MALE, 'Male'), (FEMALE, 'Female'))

    ANNUAL   = 'N'
    FREE     = 'F'
    LIFETIME = 'L'
    MEMBERSHIP_CHOICES = ( (FREE, 'Complementary'), (ANNUAL, 'Annual'), (LIFETIME, 'Life Time') )
    # CLUB_CHOICES = ( ('ALAHLY', 'Al-Ahly' ), ('ALZAMALEK', 'Al-Zamalek'), ('WADIDEGLA', 'Wadi-Degla'), ('ALJAZIRA', 'Al-Jazira'), ('NEWGIZA', 'New-Giza'), ('ALSAID', 'Al-Said') )

    User_Name            = models.OneToOneField(User, on_delete=models.CASCADE)
    memebership_code     = models.CharField(max_length = 6, unique = True)
    first_name           = models.CharField(max_length = 64, null =True, blank=True)
    last_name            = models.CharField(max_length = 32, null =True, blank=True)
    membership_start     = models.DateField(default=datetime.today)
    renewal_date         = models.DateField(auto_now=False, blank = True, null= True)
    days_left_to_renewal = models.IntegerField(editable=False)
    memebership_type     = models.CharField(max_length = 1, choices = MEMBERSHIP_CHOICES, default= ANNUAL)
    fees                 = models.PositiveIntegerField(default=0)
    active               = models.BooleanField(default = True)
    gender               = models.CharField(max_length = 4, choices = GENDER_CHOICES,default = MALE)
    birthDay             = models.DateField(auto_now=False, default = '1980-01-01')
    Age                  = models.IntegerField(editable=False)
    job_title            = models.CharField(max_length=32, blank=True, null = True)
    company              = models.CharField(max_length=32, blank=True, null = True)
    email                = models.EmailField(max_length= 128)
    email2               = models.EmailField(max_length= 128, blank = True, null = True)
    phone                = models.CharField (max_length=16, null=True, blank=True)
    phone2               = models.CharField (max_length=16, blank=True, null = True)
    fax                  = models.CharField (max_length=16, blank=True, null = True)
    al_ahly              = models.BooleanField (default = False)
    Al_Zamalek           = models.BooleanField (default = False)
    Wadi_Degla           = models.BooleanField (default = False)
    New_Giza             = models.BooleanField (default = False)
    Al_Jazira            = models.BooleanField (default = False)
    Al_Said              = models.BooleanField (default = False)
    profile_image        = models.ImageField(upload_to = 'profiles', null = True, blank = True)
    uploaded_at          = models.DateTimeField(auto_now_add = True, null = True )
    notes                = models.TextField(null=True, blank=True)
    slug                 = models.SlugField(blank = True,null= True, editable =False )



    def __str__ (self):
        print (self.memberprofile.facebook)
        return '{} {}'.format(self.first_name,self.last_name)


class SubMember(models.Model):
    MALE = 'Mr'
    FEMALE = 'Mrs'
    GENDER_CHOICES = ( (MALE, 'Male'), (FEMALE, 'Female'))

    CHILD        = 'C'
    SUN_DAUGHTER = 'SD'
    SPOUSE       = 'S'
    sub_membership_type = ( (CHILD, 'Child-Under 21'), (SUN_DAUGHTER, 'Father/Mother' ), (SPOUSE, 'Spouse') )

    main_user           = models.ForeignKey(member, on_delete=models.CASCADE, null = True, blank = True)
    sub_membership_type = models.CharField(max_length = 2, choices = sub_membership_type, default= SPOUSE)
    name                = models.CharField(max_length = 16)
    gender              = models.CharField(max_length = 4, choices = GENDER_CHOICES,default = MALE)
    birthDay            = models.DateField(default = '2000-01-01')
    job_title           = models.CharField(max_length=32, blank=True, null = True)
    company             = models.CharField(max_length=32, blank=True, null = True)
    phone               = models.CharField (max_length=64, blank=True,  null = True)
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
        instance.renewal_date = start + timedelta(days=365)
        days_left = (instance.renewal_date-today).days
        instance.days_left_to_renewal = days_left
    else:
        instance.renewal_date = today + timedelta(days=10000)
        instance.days_left_to_renewal = 10000

    instance.Age = today.year - instance.birthDay.year
    if instance.first_name == None or instance.last_name == None:
        instance.slug = slugify(str(instance.memebership_code) + ' NoFullName')
    else:
        instance.slug = slugify('{} {}'.format(instance.first_name,instance.last_name))
    print(instance.slug)


    send_mail('Test', 'Test message from seasons, user {} was just saved'.format(instance.first_name), 'cloud@buildoncloud.website', ['business@ahmed-nada.com'])


pre_save.connect(member_pre_save, sender = member)


def count_days_post_init(instance, sender, *args, **kwargs):
    today    = date.today()
    if instance.id :

        if instance.memebership_type == 'N':
            start     = instance.membership_start
            instance.renewal_date = start + timedelta(days=365)
            days_left = (instance.renewal_date-today).days
            instance.days_left_to_renewal = days_left
        else:
            instance.days_left_to_renewal = 10000
            instance.renewal_date = today + timedelta(days=10000)


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
