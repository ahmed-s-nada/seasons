"""Full_Members URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from members.views import home_page
from django.conf.urls.static import static
from django.conf import settings
# from profile.views import user_login, user_logout
from django.contrib.auth import views as auth_views
# from model_report import report

# report.autodiscover()

admin.site.site_header = "Seasons's Members admin area"
admin.site.site_title  = "Seasons"

urlpatterns = [
    path('', home_page, name = 'index'),
    path('members/', include('members.urls', namespace = 'members')),
    # path('profile/', include('profile.urls', namespace='Profile') ),
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'profile/index.html')  , name= 'logout'),
    path('login/', auth_views.LoginView.as_view(template_name = 'profile/login.html', redirect_field_name = 'members:MembersDetails' )  , name= 'login'),
    path('explorer/', include('explorer.urls')),
    path('nested_admin/', include('nested_admin.urls')),
    # path('admin_tools/', include('admin_tools.urls')),
    path('report_builder/', include('report_builder.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
