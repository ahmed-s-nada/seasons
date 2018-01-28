from django.urls import path
from registeration.views import register, index, user_login

app_name = 'registeration'
urlpatterns=[
path('', index, name = 'index'),
path('new_reg/', register, name = 'register'),
path('login/', user_login, name= 'user_login'),
]
