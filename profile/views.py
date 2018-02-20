from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, FormView, TemplateView, UpdateView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from members.models import member
from .models import memberProfile
from . serializers import MemberSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# from .forms import RegisterProfile

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






class ProfileAPI(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ Hi this is my first ModelViewSet """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    queryset = memberProfile.objects.all()

    def list(self, request):
        queryset = memberProfile.objects.all()
        serializer = MemberSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = memberProfile.objects.all()
        item = get_object_or_404(queryset, pk = pk)
        serializer = MemberSerializer(item, context={'request':request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = memberProfile.objects.all()
        item = get_object_or_404(queryset, pk = pk)
        serializer = MemberSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

#
#
# def user_login(request):
#     if request.method == 'POST':
#         userName= request.POST.get('User Name')
#         password= request.POST.get('Password')
#         user = authenticate( username = userName, password= password)
#         if user:
#             if user.is_active:
#                 login (request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse('User in not active!')
#         else:
#             return HttpResponse('Wrong username/password!')
#
# # this else (below) means that the requset is get not post so the user is trying to
# # open the login page this is why we render the login html file, the login page wil not work without this part
#     else:
#         return render(request, 'registeration/login.html')
#
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))
