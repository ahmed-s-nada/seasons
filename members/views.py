from django.shortcuts import render
from members import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, FormView, CreateView, UpdateView, DeleteView
from members.models import member

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

class dataDetails(DetailView):
    context_object_name = 'single_member'
    model = member
    template_name = 'members/details.html'
    login_required = True
