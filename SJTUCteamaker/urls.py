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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(url='/index/')),
    path('admin/', admin.site.urls),
    path('index/', mainviews.index),
    path('blog/', homeviews.blog),
    path('blog-single/<int:competition_id>/', homeviews.blogs),
    path('competition/add/', homeviews.competition_add),
    path('competition/delete/', homeviews.competition_delete),
    path('home/', homeviews.blog),
    path('personal/', mainviews.personal),
    path('team_apply/', mainviews.team_apply),
    path('team_created/', mainviews.team_created),
    path('team_join/', mainviews.team_join),
    path('login/', mainviews.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)