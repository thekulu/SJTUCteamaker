from django.shortcuts import render, HttpResponse, redirect
from home_interface.models import User, Competition, Team, Discussion
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import check_password

class CustomBackend(ModelBackend):
    def authenticate(self, request, user_id=None, user_password=None, **kwargs):
        try:
            user = User.objects.get(user_id=user_id)
            if user_password == user.user_password:  
                print("yyy")
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def custom_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_password = request.POST.get('user_password')
        user = authenticate(request, user_id=user_id, user_password=user_password)

        if user is not None:
            login(request, user)
            return redirect('/personal/')  # 重定向到登录后的页面
    return render(request, 'login.html')

# Create your views here.
def index(request):
    return render(request, "index.html")

# @login_required(login_url='/login')

def personal(request):
    return render(request, "personal.html")

def team_apply(request):
    return render(request, "team_apply.html")

def team_created(request):
    return render(request, "team_created.html")

def team_join(request):
    return render(request, "team_join.html")