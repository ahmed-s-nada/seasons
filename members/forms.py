from django import forms
from members.models import member, SubMember
from datetime import datetime, date


class member_form(forms.ModelForm):
    class Meta:
        model = member
        fields= '__all__'

    def clean_phone(self):
        if not self.cleaned_data['phone'] is None:
            dig = [str(x) for x in range(10)]
            # print (dig)
            for c in self.cleaned_data['phone']:
              # print (c)
              if not c in dig:
                    raise forms.ValidationError('Only digits Please')
        return self.cleaned_data['phone']

    def clean_phone2(self):
        if not self.cleaned_data['phone2'] is None:
            dig = [str(x) for x in range(10)]
            # print (dig)
            for c in self.cleaned_data['phone2']:
              # print (c)
              if not c in dig:
                    raise forms.ValidationError('Only digits Please')
        return self.cleaned_data['phone2']

    def clean_fax(self):
        if not self.cleaned_data['fax'] is None:
            dig = [str(x) for x in range(10)]
            # print (dig)
            for c in self.cleaned_data['fax']:
              # print (c)
              if not c in dig:
                    raise forms.ValidationError('Only digits Please')
        return self.cleaned_data['fax']




class SubMemberForm(forms.ModelForm):

    class Meta:
        model = SubMember
        fields= '__all__'


    def clean_birthDay(self):
        today = date.today()
        print (today)
        if self.cleaned_data['sub_membership_type'] ==  'C':
            age_defferance = (today - self.cleaned_data['birthDay']).days
            if age_defferance >= 7665:
                raise forms.ValidationError ('The age is over 21 years!')
        return self.cleaned_data['birthDay']


    def clean_phone(self):
        if not self.cleaned_data['phone'] is None:
            dig = [str(x) for x in range(10)]
            # print (dig)
            for c in self.cleaned_data['phone']:
              # print (c)
              if not c in dig:
                    raise forms.ValidationError('Only digits Please')
        return self.cleaned_data['phone']
