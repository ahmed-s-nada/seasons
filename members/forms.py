from django import forms
from members.models import (member, SubMemberBase, SingleParentSubmember,
                            Under21SubMeber, SpouseSubmember, SingleInLawSubmember)
from datetime import datetime, date


class member_form(forms.ModelForm):

    class Meta:
        model = member
        fields= '__all__'

    #
    # def clean_phone(self):
    #     if not self.cleaned_data['phone'] is None:
    #         dig = [str(x) for x in range(10)]
    #         # print (dig)
    #         for c in self.cleaned_data['phone']:
    #           # print (c)
    #           if not c in dig:
    #                 raise forms.ValidationError('Only digits Please')
    #     return self.cleaned_data['phone']

    # def clean_phone2(self):
    #     if not self.cleaned_data['phone2'] is None:
    #         dig = [str(x) for x in range(10)]
    #         # print (dig)
    #         for c in self.cleaned_data['phone2']:
    #           # print (c)
    #           if not c in dig:
    #                 raise forms.ValidationError('Only digits Please')
    #     return self.cleaned_data['phone2']
    #
    # def clean_fax(self):
    #     if not self.cleaned_data['fax'] is None:
    #         dig = [str(x) for x in range(10)]
    #         # print (dig)
    #         for c in self.cleaned_data['fax']:
    #           # print (c)
    #           if not c in dig:
    #                 raise forms.ValidationError('Only digits Please')
    #     return self.cleaned_data['fax']
    #
    #
    #

class SpouseSubmemberForm(forms.ModelForm):

    class Meta:
        model = SpouseSubmember
        fields= '__all__'

    #
    # def clean_phone(self):
    #     if not self.cleaned_data['phone'] is None:
    #         dig = [str(x) for x in range(10)]
    #         # print (dig)
    #         for c in self.cleaned_data['phone']:
    #           # print (c)
    #           if not c in dig:
    #                 raise forms.ValidationError('Only digits Please')
    #     return self.cleaned_data['phone']


class SingleParentSubmemberForm(forms.ModelForm):

    class Meta:
        model = SingleParentSubmember
        fields= '__all__'
    #
    #
    # def clean_phone(self):
    #     if not self.cleaned_data['phone'] is None:
    #         dig = [str(x) for x in range(10)]
    #         # print (dig)
    #         for c in self.cleaned_data['phone']:
    #           # print (c)
    #           if not c in dig:
    #                 raise forms.ValidationError('Only digits Please')
    #     return self.cleaned_data['phone']

class SingleInLawSubmemberForm(forms.ModelForm):

    class Meta:
        model = SingleInLawSubmember
        fields= '__all__'

    #
    # def clean_phone(self):
    #     if not self.cleaned_data['phone'] is None:
    #         dig = [str(x) for x in range(10)]
    #         # print (dig)
    #         for c in self.cleaned_data['phone']:
    #           # print (c)
    #           if not c in dig:
    #                 raise forms.ValidationError('Only digits Please')
    #     return self.cleaned_data['phone']


class Under21SubMeberForm(forms.ModelForm):

    class Meta:
        model = Under21SubMeber
        fields= '__all__'
    #
    # def clean_birthDay(self):
    #     today = date.today()
    #     age_defferance = (today - self.cleaned_data['birthDay']).days
    #     if age_defferance >= 7665:
    #         raise forms.ValidationError ('The age is over 21 years!')
    #     return self.cleaned_data['birthDay']
