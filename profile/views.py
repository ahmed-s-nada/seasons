from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
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



class UpdateProfile(UpdateView):
    model = memberProfile
    fields = ['facebook', 'twitter', 'instagarm', 'addetional_email']
    template_name_suffix = '_update_form'

    success_url = reverse_lazy('members:Index')


class ProfileAPI(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ Hi this is my first ModelViewSet """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    queryset = memberProfile.objects.all()

    def list(self, request):
        queryset = memberProfile.objects.filter(active=True)
        serializer = MemberSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def perform_update(self, serializer):
        if serializer.validated_data['twitter'] == '':
            instance = serializer.save(twitter = 'No Twitter account!')
