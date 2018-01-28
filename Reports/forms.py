from django import forms
from Product.models import Product, ProductCategory, ProductsTag


class AdvancedSearchForm(forms.Form):

    cats = [x.title for x in ProductCategory.objects.all()]
    cats.insert(0,'')
    cat_choices = tuple(zip(cats, cats))
    tags = [x.title for x in ProductsTag.objects.all()]
    tags.insert(0,'')
    tag_choices = tuple(zip(tags, tags))
    product_name = forms.CharField(max_length=64, required = False)
    category     = forms.ChoiceField(choices = cat_choices, required=False)
    tag          = forms.ChoiceField(choices = tag_choices, required=False)
    maker        = forms.CharField(max_length=64, required = False)
    min_price    = forms.IntegerField(required = False)
    max_price    = forms.IntegerField(required = False)
    featured     = forms.BooleanField(required = False)
    # cat          = forms.CharField(max_length = 64, blank = True, widget = forms.ChoiceWidget)


    # def clean_min_price(self):
    #     min_price = self.cleaned_data.get('min_price')
    #     max_price = self.cleaned_data.get('max_price')
    #     # if max_price is None or max_price == 0 or max_price == '':
    #     #     raise forms.ValidationError('You must enter a max price!')
    #
    #     if min_price >= max_price:
    #         raise forms.ValidationError('Max price must be higher than min price!')
    #
    #     return min_price
    #
    # def clean_max_price(self):
    #     min_price = self.cleaned_data.get('min_price')
    #     max_price = self.cleaned_data.get('max_price')
    #     # if min_price is None or min_price == '':
    #     #     raise forms.ValidationError('You must enter a min price! {}'.format(min_price))
    #
    #     if min_price >= max_price:
    #         raise forms.ValidationError('Max price must be higher than min price!')
    #
    #     return max_price
