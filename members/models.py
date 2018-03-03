from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_init, post_delete, pre_delete
from datetime import date, datetime, timedelta
# from .forms import member_form
from django.utils.text import slugify
from django.core.mail import send_mail
import string, secrets
from . validators import clean_phone
from django.db.models import Q


# The member section *********************************************************************

class MemberQuerySet(models.query.QuerySet):

    def get_female(self):
        return self.filter(gender='Mrs')

    def get_male(self):
        return self.filter(gender='Mr')

    def get_age_range(self, min_age, max_age):
        return self.filter(age__lte = max_age).filter(age__gte=min_age)

    def search (self, query):
        lookups = Q(first_name__icontains = query )| Q(memebership_code__icontains = query )
        print('from search in queryset ', query)
        return self.filter(lookups)



class MemberManager(models.Manager):

    def get_queryset(self):
        return MemberQuerySet(self.model, using= self._db)

    def search(self, query):
        return self.get_queryset().search(query)



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

    User_Name            = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, related_name='member_account', editable = False)
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
    age                  = models.IntegerField(editable=False)
    job_title            = models.CharField(max_length=32, blank=True, null = True)
    company              = models.CharField(max_length=32, blank=True, null = True)
    email                = models.EmailField(max_length= 128)
    # email2               = models.EmailField(max_length= 128, blank = True, null = True)
    phone                = models.CharField (validators=[clean_phone], max_length=16, null=True, blank=True)
    phone2               = models.CharField (validators=[clean_phone], max_length=16, blank=True, null = True)
    fax                  = models.CharField (validators=[clean_phone], max_length=16, blank=True, null = True)
    al_ahly              = models.BooleanField (default = False)
    Al_Zamalek           = models.BooleanField (default = False)
    Wadi_Degla           = models.BooleanField (default = False)
    New_Giza             = models.BooleanField (default = False)
    Al_Jazira            = models.BooleanField (default = False)
    Al_Said              = models.BooleanField (default = False)
    profile_image        = models.ImageField(upload_to = 'profiles', null = True, blank = True)
    uploaded_at          = models.DateTimeField(auto_now_add = True, null = True )
    notes                = models.TextField(null=True, blank=True)
    password             = models.CharField(max_length = 512, default='abcd1234')
    facebook             = models.URLField(verbose_name= 'Facebook', blank = True, null = True)
    twitter              = models.URLField(verbose_name= 'Twitter', blank = True, null = True)
    instagarm            = models.URLField(verbose_name= 'Instagram', blank = True, null = True)
    addetional_email     = models.EmailField(blank = True, null = True)
    slug                 = models.SlugField(blank = True,null= True, editable =False )
    no_of_submembers     = models.PositiveIntegerField(blank=True, default=0, editable = False)


    objects = MemberManager()

    def save(self, *args, **kwargs):
        # if self.member_account == None:
        if self._state.adding == True: # <== Chicking if the object is new and being added to the DB
            username= self.first_name[0].upper() + '_' + self.last_name + '_' + str(self.memebership_code)

            char_classes = (string.ascii_lowercase,
                        string.ascii_uppercase,
                        string.digits,
                        string.punctuation)
            size = lambda: secrets.choice(range(8,9))                  # Chooses a password length.
            char = lambda: secrets.choice(secrets.choice(char_classes)) # Chooses one character, uniformly selected from each of the included character classes.
            pw = lambda: ''.join([char() for _ in range(size())])     # Generates the variable-length password.
            password = pw()
            qs = User.objects.filter(username = username)
        # print (qs)
            # if qs.count() == 0:
            user = User.objects.create_user(username = username, password = password)
            self.User_Name = user
            self.password= user.password
            send_mail('Member Details', 'Hi! This is your login details:\nUsername: {} \nPassword: {} \n'.format(username, password),
                      'cloud@buildoncloud.website', ['business@ahmed-nada.com'])

        super(member, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('members:MembersDetails', kwargs={'slug': self.slug})


    def __str__ (self):
        # print (self.memberprofile.facebook)
        return '{} {}'.format(self.first_name,self.last_name)




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

    instance.age = today.year - instance.birthDay.year
    if instance.first_name == None or instance.last_name == None:
        instance.slug = slugify(str(instance.memebership_code) + ' NoFullName')
    else:
        instance.slug = slugify('{} {}'.format(instance.first_name,instance.last_name))
    # print(instance.slug)

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



def member_post_delete(instance, sender, *args, **kwargs):

    if not instance.User_Name.is_superuser:
        user = User.objects.get(username = instance.User_Name)
        print(user)
        user.delete()
post_delete.connect(member_post_delete, sender=member)

# End of The member section ************************************************************


# The Submember classes section *********************************************************

class SubMemberBase(models.Model):
    MALE = 'Mr'
    FEMALE = 'Mrs'
    GENDER_CHOICES = ( (MALE, 'Male'), (FEMALE, 'Female'))

    main_member         = models.ForeignKey(member, on_delete=models.CASCADE, null = True, blank = True)
    # sub_membership_type = models.CharField(max_length = 2, choices = sub_membership_type, default= SPOUSE)
    first_name          = models.CharField(max_length = 18)
    last_name           = models.CharField(max_length = 16)
    gender              = models.CharField(max_length = 4, choices = GENDER_CHOICES,default = MALE)
    birthDay            = models.DateField(default = '2000-01-01')
    age                 = models.PositiveIntegerField(editable=False)
    profile_image       = models.ImageField(upload_to = 'profiles', null = True, blank = True)
    sub_member_active   = models.BooleanField(default = True)

    class Meta:
         abstract = True

    def __str__ (self):
        return '{} {}'.format(self.first_name, self.last_name)


def sub_member_counter_pre_save(instance, sender, *args, **kwargs):

    today    = date.today()
    instance.age = today.year - instance.birthDay.year
    if instance._state.adding == True:  # <= cheking if the object is new not an existing one
        if isinstance (instance, SingleInLawSubmember):
            spouse = SpouseSubmember.objects.get(id=instance.main_sub_member.id)
            print (spouse)
            main_member = member.objects.get(id=spouse.main_member.id)
            instance.main_member = main_member
        else:
            main_member = member.objects.get(id=instance.main_member.id)
        main_member.no_of_submembers = main_member.no_of_submembers + 1
        main_member.save()



def sub_member_counter_pre_delete(instance, sender, *args, **kwargs):

    if isinstance(instance, SpouseSubmember):
        if instance.singleinlawsubmember_set.all().count() != 0:
            pass
        else:
            main_member = member.objects.get(id=instance.main_member.id)
            main_member.no_of_submembers = main_member.no_of_submembers - 1
            main_member.save()
    else:
        main_member = member.objects.get(id=instance.main_member.id)
        main_member.no_of_submembers = main_member.no_of_submembers - 1
        main_member.save()



class SingleParentSubmember(SubMemberBase):

    job_title           = models.CharField(max_length=32, blank=True, null = True)
    company             = models.CharField(max_length=32, blank=True, null = True)
    phone               = models.CharField (validators=[clean_phone], max_length=64, blank=True,  null = True)
    email               = models.EmailField(max_length= 128,  null = True)

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parent'

pre_save.connect(sub_member_counter_pre_save, sender = SingleParentSubmember)
pre_delete.connect(sub_member_counter_pre_delete, sender = SingleParentSubmember)



class Under21SubMeber(SubMemberBase):

    School              = models.CharField(max_length=32, blank=True, null = True)
    Grade               = models.CharField(max_length=32, blank=True, null = True)
    Sport               = models.CharField (max_length=64, blank=True,  null = True)

    class Meta:
        verbose_name = 'Child Under 21'
        verbose_name_plural = 'Children Under 21'

pre_save.connect(sub_member_counter_pre_save, sender = Under21SubMeber)
pre_delete.connect(sub_member_counter_pre_delete, sender = Under21SubMeber)


class SpouseSubmember(SubMemberBase):

    job_title           = models.CharField(max_length=32, blank=True, null = True)
    company             = models.CharField(max_length=32, blank=True, null = True)
    phone               = models.CharField (validators=[clean_phone], max_length=64, blank=True,  null = True)
    email               = models.EmailField(max_length= 128,  null = True)

    class Meta:
        verbose_name = 'Spouse'
        verbose_name_plural = 'Spouse'

pre_save.connect(sub_member_counter_pre_save, sender = SpouseSubmember)
pre_delete.connect(sub_member_counter_pre_delete, sender = SpouseSubmember, dispatch_uid='Spouseid')



class SingleInLawSubmember(SubMemberBase):

    main_sub_member     = models.ForeignKey(SpouseSubmember, on_delete=models.CASCADE, null = True, blank = True)
    job_title           = models.CharField(max_length=32, blank=True, null = True)
    company             = models.CharField(max_length=32, blank=True, null = True)
    phone               = models.CharField (validators=[clean_phone], max_length=64, blank=True,  null = True)
    email               = models.EmailField(max_length= 128,  null = True)
    # user = User.objects.create_user()
    class Meta:
        verbose_name = 'In-Law'
        verbose_name_plural = 'In-Law'

pre_save.connect(sub_member_counter_pre_save, sender = SingleInLawSubmember)
pre_delete.connect(sub_member_counter_pre_delete, sender = SingleInLawSubmember, dispatch_uid='In_law_id')


# END OF The Submember classes section **********************************************************


# The Paymnet section ***************************************************************************

class Payment(models.Model):

    methodes = (('CASH', 'Cash'), ('CRIDIT', 'VISA/MASTER'), ('CHEQUE', 'Cheque'))
    member               = models.ForeignKey(member, on_delete=models.CASCADE)
    # payment_methode      = models.CharField(max_length = 11, choices = methodes)
    payment_details      = models.CharField(max_length = 128, blank = True)
    last_payment_date    = models.DateField(auto_now=False, blank = True, null = True)
    required_fees        = models.PositiveIntegerField(default=0)
    payments_total       = models.PositiveIntegerField (blank=True, default = 0, editable=False)
    current_credit       = models.IntegerField(default=0, editable=False)
    number_of_Instalment = models.PositiveIntegerField(editable=False, default= 1)

    def __str__(self):
        return "Payment of {} by: {}".format(self.payments_total,self.member)


class Instalment(models.Model):

    methodes = (('CASH', 'Cash'), ('CRIDIT', 'VISA/MASTER'), ('CHEQUE', 'Cheque'))

    payment_file       = models.ForeignKey(Payment, related_name='instalments', on_delete=models.CASCADE)
    payment_methode    = models.CharField(max_length = 11, choices = methodes)
    instalment_details = models.CharField(max_length = 128, blank = True)
    instalment_date    = models.DateField(auto_now=False, blank = True,  default = date.today())
    instalment_value   = models.PositiveIntegerField (blank = True, default = 0)

    def __str__(self):
        return 'Instalment paid on: {}'.format(self.instalment_date)


def payment_post_init(instance, sender, *args, **kwargs):
    instalments= instance.instalments.all()

    temp_total = 0
    instance.number_of_Instalment = instalments.count()
    for i in instalments:
        temp_total = temp_total + i.instalment_value
    instance.payments_total    = temp_total
    instance.current_credit    = instance.payments_total - instance.required_fees
    if instalments.count() > 0 :
        instance.last_payment_date = instalments[instalments.count() - 1].instalment_date


post_init.connect(payment_post_init, sender = Payment)

# End of The Paymnet section *************************************************************
