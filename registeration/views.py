from django.shortcuts import render
from registeration.forms import userProfileInfoForm, userForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def index(request):
    return render(request, 'registeration/index.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = userForm(data = request.POST)
        profile_form = userProfileInfoForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid() :
            theUser = user_form.save()
            theUser.set_password(theUser.password)
            theUser.save()

            theProfile = profile_form.save(commit = False)
            theProfile.user = theUser

            if 'favPhoto' in request.FILES:
                theProfile.favPhoto = request.FILES['favPhoto']

            theProfile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = userForm()
        profile_form = userProfileInfoForm()

    return render (request, 'registeration/reg.html',context= {'registered': registered,
                                                               'user_form': user_form,
                                                                'profile_form': profile_form} )



def user_login(request):
    if request.method == 'POST':
        userName= request.POST.get('User Name')
        password= request.POST.get('Password')
        user = authenticate( username = userName, password= password)
        if user:
            if user.is_active:
                login (request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('User in not active!')
        else:
            return HttpResponse('Wrong username/password!')

# this else (below) means that the requset is get not post so the user is trying to
# open the login page this is why we render the login html file, the login page wil not work without this part
    else:
        return render(request, 'registeration/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
