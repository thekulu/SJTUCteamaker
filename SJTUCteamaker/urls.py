"""
URL configuration for mysite2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from home_interface import views as homeviews
from main_interface import views as mainviews
from team_interface import views as teamviews
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/index/')),
    path('admin/', admin.site.urls),
    path('index/', mainviews.index),
    path('blog/', homeviews.blog),
    path('blog-single/', homeviews.blogs),
    path('home/', homeviews.blog),
    path('personal/', mainviews.personal),
    path('team_apply/', mainviews.team_apply),
    path('team_created/', mainviews.team_created),
    path('team_join/', mainviews.team_join),
    path('login/', mainviews.custom_login, name='login'),
    path('register/', mainviews.reg),
]