from django.contrib import admin
from django import forms
from datetime import date, datetime
from members.models import member, SubMember, Payment, Instalment
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from .forms import member_form, SubMemberForm
from django.utils.html import format_html
from .admin_image_classes import AdminImageWidget, ImageWidgetAdmin
from profile.models import memberProfile
from import_export.admin import ImportExportMixin


class InstalmentInline(NestedTabularInline):
    model = Instalment
    extra = 0
    max_num = 4


class PaymentInline (NestedStackedInline):
    model = Payment
    extra = 1
    max_num = 1
    inlines = [InstalmentInline,]
    readonly_fields =['number_of_Instalment', 'payments_total', 'current_credit', 'last_payment_date']



class memberProfileInline(NestedStackedInline):

    model = memberProfile
    extra = 0
    max_num = 1

    fieldsets = (
        ('Extended profile',{
            'classes': ('collapse',),
            'fields': ('active', 'addetional_email', ('facebook', 'twitter', 'instagarm'))
        }),)




class SubMemberInline(NestedStackedInline):

    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="240" height="300"/>'.format(obj.profile_image.url))
        else:
            return 'None'
    image_tag.short_description = 'Image'


    model = SubMember
    form = SubMemberForm
    extra = 0
    max_num = 5

    # fields = ['sub_membership_type', 'name', 'gender', 'birthDay','phone']
    fieldsets = (
    (None , {

        'fields':( ('sub_membership_type', 'sub_member_active'))
    }),
    (
    None ,{

        'fields' : ( ('name' , 'gender', 'birthDay'),
                   ('job_title', 'company'), ('phone', 'email'), 'image_tag', 'profile_image',)

    })
    )
    readonly_fields = ['image_tag']


class SubMemberAdmin(ImageWidgetAdmin, admin.ModelAdmin):

    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" height="100"/>'.format(obj.profile_image.url))
        else:
            return 'None'
    image_tag.short_description = 'Image'

    image_fields    = ['profile_image']
    search_fields   = ['main_user', 'name']
    list_display    = ['main_user', 'name', 'gender', 'sub_membership_type','phone','image_tag']
    list_filter     = ['gender', 'sub_membership_type']

    class Meta:
        model = SubMember



class InputFilterNoOfSubmembers(admin.SimpleListFilter):
    template = 'admin/input_filter.html'
    title = ('Number of SubMembers')

    parameter_name = 'no_of_submembers'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


    def queryset(self, request, queryset):
        if self.value() != None:
            v = self.value()
            while True:
                try:
                    userInput = int(v)
                    return queryset.filter(no_of_submembers = userInput )
                except ValueError:
                   print("{} Not an integer! Try again.".format(v))
                   break


class FilterByAgeGroup(admin.SimpleListFilter):
    title = 'Age Group'
    parameter_name = 'age_group'

    def lookups(self, request, model_admin):
        return (
            ('21_30', 'From 21 to 30 years'),
            ('31_40', 'From 31 to 40 years'),
            ('41_50', 'From 41 to 50 years'),
            ('51_60', 'From 51 to 60 years'),
            ('over_60', 'Over 60 Years')
            )

    def queryset(self, request, queryset):
        if self.value() == '21_30':
            return queryset.filter(Age__gte = 21).filter(Age__lte=30)
        if self.value() == '31_40':
            return queryset.filter(Age__gte = 31).filter(Age__lte=40)
        if self.value() == '41_50':
            return queryset.filter(Age__gte = 41).filter(Age__lte=50)
        if self.value() == '51_60':
            return queryset.filter(Age__gte = 51).filter(Age__lte=60)
        if self.value() == 'over_60':
            return queryset.filter(Age__gte = 61)



def mark_as_active(modeladmin, request, queryset):
    queryset.update(active = True)

mark_as_active.short_description = 'Actiavte selected memberships'


def mark_as_inactive(modeladmin, request, queryset):
    queryset.update(active = False)

mark_as_inactive.short_description = 'Dectiavte selected memberships'


class memberAdmin(ImportExportMixin, ImageWidgetAdmin, NestedModelAdmin ):

    form = member_form

    image_fields = ['profile_image']

    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" height="100"/>'.format(obj.profile_image.url))
        else:
            return 'None'

    image_tag.short_description = 'Image'


    search_fields   = ('first_name', 'last_name','memebership_code' )
    inlines         = [PaymentInline, memberProfileInline, SubMemberInline, ]
    list_display    = ('first_name','last_name', 'memebership_code', 'membership_start',
                       'renewal_date', 'days_left_to_renewal', 'memebership_type', 'active', 'image_tag')
    list_filter     = ('memebership_type', 'membership_start', 'renewal_date',
                        'active', InputFilterNoOfSubmembers, 'gender', FilterByAgeGroup, )
    readonly_fields = ['User_Name', 'days_left_to_renewal', 'uploaded_at', 'Age', 'no_of_submembers']
    actions         = [mark_as_active, mark_as_inactive]

    fieldsets = (
      ('Membership info', {
          'fields': (('User_Name', 'memebership_code'),('first_name','last_name'),
                     ('membership_start' ,'renewal_date', 'days_left_to_renewal'),
             ( 'memebership_type', 'active'),'no_of_submembers',)
      }),
      ('Personal info', {
          'classes': ('collapse',),
          'fields': ('gender', ('birthDay', 'Age'), ('job_title', 'company'), ('email', 'email2'), ('phone',
              'phone2', 'fax'), 'profile_image', 'uploaded_at' ,'notes')
      }),('Other Club Memberships', {
          'classes': ('collapse','extrapretty',),
          'fields': ('al_ahly', 'Al_Zamalek', 'Wadi_Degla', 'New_Giza', 'Al_Jazira', 'Al_Said')
      }),
   )



    class Meta:
        model = member



admin.site.register(member, memberAdmin)
admin.site.register(SubMember, SubMemberAdmin)
