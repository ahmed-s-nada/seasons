from django import forms
from members.models import member

class member_form(forms.ModelForm):
    class Meta:
        model = member
        fields = "__all__"
        
