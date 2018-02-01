from django.contrib import admin
from django import forms
from datetime import date, datetime
from members.models import member, SubMember
from .forms import member_form, SubMemberForm
from django.utils.html import format_html
from .admin_image_classes import AdminImageWidget, ImageWidgetAdmin



class SubMemberInline(admin.StackedInline):

    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="300" height="300"/>'.format(obj.profile_image.url))
        else:
            return 'None'
    image_tag.short_description = 'Image'


    model = SubMember
    form = SubMemberForm
    extra = 0
    max_num = 5
    # fields = ['sub_membership_type', 'name', 'gender', 'birthDay','phone']
    fieldsets = (
    ('SubMember info', {
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

    image_fields = ['profile_image']

    list_display = ['main_user', 'name', 'gender', 'sub_membership_type','phone','image_tag']
    list_filter  = ['main_user', 'name', 'gender', 'sub_membership_type','phone']

    class Meta:
        model = SubMember




class memberAdmin(ImageWidgetAdmin, admin.ModelAdmin):

    form = member_form

    image_fields = ['profile_image']

    def image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" height="100"/>'.format(obj.profile_image.url))
        else:
            return 'None'

    image_tag.short_description = 'Image'

    fieldsets = (
      ('Membership info', {
          'fields': (('User_Name','memebership_code'),('first_name','last_name'),('membership_start' ,'renewal_date', 'days_left_to_renewal'),
             ( 'memebership_type', 'fees', 'active'),)
      }),
      ('Personal info', {
          'fields': ('gender', ('birthDay', 'Age'), ('job_title', 'company'), ('email', 'email2'), ('phone',
              'phone2', 'fax'), 'profile_image', 'uploaded_at' ,'notes')
      }),
   )


    search_fields   = ('first_name', 'last_name','memebership_code', 'membership_start', 'renewal_date', 'days_left_to_renewal', 'active' )
    inlines         = [ SubMemberInline ]
    list_display    = ('first_name','last_name', 'memebership_code', 'membership_start', 'renewal_date', 'days_left_to_renewal', 'memebership_type', 'active', 'image_tag')
    list_filter     = ('gender', 'membership_start', 'renewal_date', 'memebership_type')
    readonly_fields = ['days_left_to_renewal', 'uploaded_at', 'Age']

    class Meta:
        model = member




admin.site.register(member, memberAdmin)
admin.site.register(SubMember, SubMemberAdmin)
