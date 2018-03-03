from django import forms
from django.contrib.auth.models import User
from .models import memberProfile
from members.models import member


# class RegisterProfile(forms.ModelForm):
#     memebership_code = forms.CharField(max_length=8)
#     password         = forms.CharField (widget = forms.PasswordInput() )
#     class Meta:
#         model = memberProfile
#         exclude = ['active',]
#



class userProfileInfoForm(forms.ModelForm):
    class Meta():
        model = userProfileInfo
        fields = ('facebook', 'twitter', 'instagarm', 'addetional_email')
