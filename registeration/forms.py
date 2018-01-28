from django import forms
from django.contrib.auth.models import User
from registeration.models import userProfileInfo


class userForm(forms.ModelForm):
    password = forms.CharField (widget = forms.PasswordInput() )
    class Meta():
        model = User
        fields = ('username', 'email', 'password')



class userProfileInfoForm(forms.ModelForm):
    class Meta():
        model = userProfileInfo
        fields = ('favSite', 'favPhoto')
