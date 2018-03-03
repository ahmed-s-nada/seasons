from django.urls import path, include
from members.views import (member_form, listData, MembersDetails, index, InstalmentiAPIView,
                           PaymentApiView, SearchMemberView, UpdateMemberProfile, ProfileAPI)
from profile.views import UpdateProfile
from django.contrib.auth.decorators import login_required
from rest_framework import routers

router = routers.DefaultRouter()
router.register('PaymentAPI', PaymentApiView, base_name='Payments')
router.register('InstallmentAPI', InstalmentiAPIView)
router.register('members', ProfileAPI, base_name='Members')

app_name = 'members'
instalment_list=InstalmentiAPIView.as_view({'get':'list'})
instalment_detail=InstalmentiAPIView.as_view({'get':'retrieve'})

payment_list=PaymentApiView.as_view({'get':'list'})
payment_detail=PaymentApiView.as_view({'get':'retrieve'})

update_profile=ProfileAPI.as_view({'put':'partial_update'})
member_list=ProfileAPI.as_view({'get':'list'})
member_detail=ProfileAPI.as_view({'get':'retrieve'})

urlpatterns = [

        path('', index, name='Index' ),
        path('add/', member_form, name = 'mainForm'),
        path('list/', login_required(listData.as_view()), name= 'listData'),
        path('search/<slug:slug>/', login_required(MembersDetails.as_view()), name= 'MembersDetails'),
        path('search/update/<int:pk>/',login_required(UpdateMemberProfile.as_view()), name='Update' ),
        path('search/', login_required(SearchMemberView.as_view()), name= 'Search'),
        path('api/', include(router.urls)),
        path('api/list/',  member_list, name='member-list'),
        path('api/<int:pk>/', member_detail, name='member-detail'),
        path('api/update/<int:pk>', update_profile, name='updateprofile'),
        path('api/instalments', instalment_list, name='instalment-list'),
        path('api/instalment/<int:pk>', instalment_detail, name='instalment-detail'),
        path('api/payments', payment_list, name='payment-list'),
        path('api/payment/<int:pk>/', payment_detail, name='payment-detail'),
]
