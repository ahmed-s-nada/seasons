from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from members import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import (DetailView, ListView, FormView, CreateView,
                                  UpdateView, DeleteView)
from members.models import member, Payment, Instalment
from django.http import Http404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   RetrieveModelMixin, Response, UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .serializers import PaymentSerializer, InstallmentSerializer, MemberSerializer

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
            print ("The member's full name is: {} {}".format(myForm.cleaned_data['First_Name'] ,
                                                             myForm.cleaned_data['Last_Name'] ))
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
        print (instance.memebership_type)
        if instance is None :
            raise Http404('No such member!')
        # print (instance.spousesubmember_set.all().first().profile_image.url)
        # print (instance.first_name)
        return instance

    login_required = True

class SearchMemberView(ListView):
    context_object_name = 'all_members'
    template_name = 'members/member_list.html'
    model = member
    kw = ''

    def get_queryset(self, *args, **kwargs):
        request = self.request
        self.kw = request.GET.get('q')
        print('q= ', self.kw)
        if self.kw is not None and self.kw != '':
            return member.objects.search(self.kw)
        else:
            return member.objects.all()


    def get_context_data(self, *args, **kwargs):
        context = super(SearchMemberView, self).get_context_data(*args, **kwargs)
        if  self.kw != '':
            context['header'] = 'Search results...'
            context['q'] = self.kw
        else:
            context['header'] = 'No results!\n Check the full list: '
            # context['q'] = self.query
        return context


class UpdateMemberProfile(UpdateView):
    model = member
    fields = ['facebook', 'twitter', 'instagarm', 'addetional_email']
    template_name = 'members/member_update_form.html'
    success_url = reverse_lazy('members:listData')

    def get_context_data(self, *args, **kwargs):
        contexet =super(UpdateMemberProfile, self).get_context_data(*args, **kwargs)
        # context['member'] = member.objects.filter(slug = slug).first()
        print(contexet)
        return contexet


# -----------------------------------------------------------------------------


class ProfileAPI(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ Hi this is my first ModelViewSet """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberSerializer
    queryset = member.objects.all()

    def list(self, request):
        # queryset = member.objects.filter(active=False)
        queryset = member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = member.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MemberSerializer(item)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = member.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = MemberSerializer(item)
        return Response(serializer.data)

    # def perform_update(self, serializer):
    #     if serializer.validated_data['twitter'] == '':
    #         instance = serializer.save(twitter = 'No Twitter account!')

class PaymentApiView(UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def list(self, request):
        queryset = Payment.objects.all()
        serializer = PaymentSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Payment.objects.all()
        item = get_object_or_404(queryset, pk=pk, context={'request':request})
        serializer = PaymentSerializer(item)
        return Response(serializer.data)



class InstalmentiAPIView(UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = InstallmentSerializer
    queryset = Instalment.objects.all()

    def list(self, request):
        queryset = Instalment.objects.all()
        serializer = InstallmentSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Instalment.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = InstallmentSerializer(item, context={'request':request})
        return Response(serializer.data)



# class InstalmentListAPIView(ListAPIView):
#     queryset = Instalment.objects.all()
#     serializer_class = InstallmentSerializer
#     # permission_classes = [AllowAny]
#     # filter_backends = [SearchFilter, OrderingFilter]
#     # search_fields = ['title', 'slug']
#
#
# class InstalmentDetailAPIView(RetrieveAPIView):
#     queryset = Instalment.objects.all()
#     serializer_class = InstallmentSerializer
#     # permission_classes = [AllowAny]
#
#
