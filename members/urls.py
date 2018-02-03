from django.urls import path
from members.views import member_form, listData, MembersDetails, index
from django.contrib.auth.decorators import login_required
app_name = 'members'

urlpatterns = [

        path('', index, name='Index' ),
        path('add/', member_form, name = 'mainForm'),
        path('list/', login_required(listData.as_view()), name= 'listData'),
        path('list/<slug:slug>/', login_required(MembersDetails.as_view()), name= 'MembersDetails'),
]
