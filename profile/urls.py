from django.urls import path
from profile.views import index, ProfileReg

app_name = 'profile'
urlpatterns=[
path('', index, name = 'index'),
path('reg/', ProfileReg.as_view(), name = 'register'),
# path('login/', user_login, name= 'user_login'),
]
