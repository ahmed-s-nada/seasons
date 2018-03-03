from django.urls import path, include
# from profile.views import index, ProfileReg
from rest_framework import routers
from . views import ProfileAPI, UpdateProfile
from django.contrib.auth.decorators import login_required


router = routers.DefaultRouter()
router.register('list', ProfileAPI)


app_name = 'profile'
urlpatterns=[
# path('', index, name = 'index'),
path('update/<int:pk>/', login_required(UpdateProfile.as_view()), name= 'UpdateProfile'),
path('api/', include(router.urls)),
# path('login/', user_login, name= 'user_login'),
]
