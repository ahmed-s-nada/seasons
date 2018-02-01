from django.shortcuts import render
from members import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, FormView, CreateView, UpdateView, DeleteView
from members.models import member
from django.http import Http404

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'members/index.html')

@login_required
def member_form(request):
    myForm = forms.member_form()
    if request.method == 'POST':
        myForm = forms.member_form(request.POST, request.FILES)
        if myForm.is_valid():
            myForm.save()
            print ("The member's full name is: {} {}".format(myForm.cleaned_data['First_Name'] , myForm.cleaned_data['Last_Name'] ))
            return home_page(request)
    return render(request, 'members/form.html', context={'members': myForm})

class listData(ListView):
    context_object_name = 'all_members'
    model = member
    login_required = True

class MembersDetails(DetailView):

    model = member
    context_object_name = 'single_member'
    template_name = 'members/details.html'
    # template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        contexet =super(MembersDetails, self).get_context_data(*args, **kwargs)
        # context['member'] = member.objects.filter(slug = slug).first()
        print(contexet)
        return contexet

    def get_object(self, *args, **kwargs): # <== overriding the get_object to put our 404 message
        # request = self.request
        slug = self.kwargs.get('slug')
        print (slug)
        instance  = member.objects.filter(slug = slug).first()
        if instance is None :
            raise Http404('No such member!')
        print (instance.submember_set.all().first().profile_image.url)
        print (instance.first_name)
        return instance

    login_required = True
