from django.urls import path, include
# from profile.views import index, ProfileReg
from rest_framework import routers
from . views import ProfileAPI

router = routers.DefaultRouter()
router.register('list', ProfileAPI)


app_name = 'profile'
urlpatterns=[
# path('', index, name = 'index'),
# path('reg/', ProfileReg.as_view(), name = 'register'),
path('api/', include(router.urls)),
# path('login/', user_login, name= 'user_login'),
]
