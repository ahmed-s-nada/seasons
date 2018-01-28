from django.shortcuts import render
from django.views.generic import ListView, FormView
from Product.models import Product
from .forms import AdvancedSearchForm
from django.shortcuts import render

# Create your views here.

class SearchProductView(ListView):
    template_name = 'Product/product_list.html'
    model = Product
    kw = ''

    def get_queryset(self, *args, **kwargs):
        request = self.request
        self.kw = request.GET.get('q')

        if self.kw is not None and self.kw != '':
            return Product.objects.search(self.kw)
        else:
            return Product.objects.get_queryset().featured()


    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        if  self.kw != '':
            context['header'] = 'Search results...'
            context['q'] = self.kw
        else:
            context['header'] = 'No results!\n Check theses great offers'
            # context['q'] = self.query
        return context


class AdvancedSearch(FormView):     # <= using FormView to handle form data
    form_class = AdvancedSearchForm
    template_name = 'Product/form.html'

    def get_context_data(self , *args, **kwargs):
        context = super(AdvancedSearch, self).get_context_data(*args, **kwargs)
        context['content'] = 'Enter search details'
        context['header'] = 'Welcome to the Advanced Search'
        return context


    def post(self, request, *args, **kwargs): # <= this is how you handle a form: by overriding post

        form = self.get_form()                # <= get the form object

        if form.is_valid():                   # <= check that the form is valid

            product_name    = form.cleaned_data.get('product_name') # <= collect data from fields
            cat             = form.cleaned_data.get('category')     # <= Always use 'cleaned_data' then 'get'
            tag             = form.cleaned_data.get('tag')
            maker           = form.cleaned_data.get('maker')
            min_price       = form.cleaned_data.get('min_price')
            # print (min_price)
            max_price       = form.cleaned_data.get('max_price')
            # print (max_price)
            featured        = form.cleaned_data.get('featured')

            results = Product.objects.all()

            if product_name is not None and product_name != '':
                results = results.search(product_name)
            if cat is not None and cat != '':
                results = results.search_by_cat(cat)
            if tag is not None and tag != '':
                results = results.search_by_tag(tag)
            if maker is not None and maker != '':
                results = results.search_maker(maker)
            if min_price is not None and max_price is not None :
                # print (min_price, max_price)
                # print(results)
                results = results.search_price_range(min_price, max_price)
                # print (results)
            if featured is True:
                results = results.featured()
            # if product_name is not None and product_name != '':
            #     results = results.search(product_name)

            return render(request, 'Product/product_list.html', {'product_list': results, 'header': 'Adanced Search Results'})
        else:
            return self.form_invalid(form)
