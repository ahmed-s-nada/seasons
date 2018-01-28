from django.contrib import admin
from members.models import member, SubMember
from django import forms
from datetime import date, datetime

# Register your models here.


class SubMemberForm(forms.ModelForm):
    class Meta:
        model = SubMember
        fields= '__all__'

    def clean_birthDay(self):
        today = date.today()
        print (today)
        if self.cleaned_data['sub_membership_type'] ==  'C':
            age_defferance = (today - self.cleaned_data['birthDay']).days
            if age_defferance >= 4380:
                raise forms.ValidationError ('The age is over 12 years!')
        return self.cleaned_data['birthDay']


class SubMemberInline(admin.TabularInline):
    model = SubMember
    form = SubMemberForm
    extra = 0
    max_num = 4
    fields = ['sub_membership_type', 'name', 'gender', 'birthDay','phone']
    # fieldsets =

class memberAdmin(admin.ModelAdmin):
    fields = ['User_Name','memebership_code','Name','membership_start' ,'renewal_date', 'days_left_to_renewal',
              'memebership_type','active', 'gender', 'birthDay', 'Age', 'job_title', 'company', 'email', 'email2', 'phone',
              'phone2', 'fax', 'profile_image', 'uploaded_at' ,'notes' ]
    search_fields   = ('Name', 'memebership_code', 'membership_start', 'renewal_date', 'active' )
    inlines         = [ SubMemberInline ]
    list_display    = ('Name','memebership_code', 'membership_start', 'renewal_date', 'memebership_type', 'active')
    list_filter     = ('Name','memebership_code', 'membership_start', 'renewal_date', 'memebership_type', 'active')
    readonly_fields = ['days_left_to_renewal', 'uploaded_at', 'Age']

    class Meta:
        model = member



class SubMemberAdmin(admin.ModelAdmin):
    # form = SubMemberForm
    list_display = ['main_user', 'name', 'gender', 'sub_membership_type','phone']
    list_filter  = ['main_user', 'name', 'gender', 'sub_membership_type','phone']

    class Meta:
        model = SubMember

admin.site.register(member, memberAdmin)
admin.site.register(SubMember, SubMemberAdmin)
