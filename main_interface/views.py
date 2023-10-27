from django import http
from django.contrib.auth.decorators import login_required
from home_interface.models import User, Competition, Team
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from home_interface.forms import UserForm
# from django.contrib.auth.hashers import check_password
class CustomBackend(ModelBackend):
    def authenticate(self, request, user_id=None, user_password=None, **kwargs):
        try:
            user = User.objects.get(user_id=user_id)
            if user_password == user.user_password:
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
        next_url = request.POST.get("next_url")
        if next_url and next_url != "/logout/":
            response = redirect(next_url)
        else:
            response = redirect("/index/")
        user = authenticate(request, user_id=user_id, user_password=user_password)
        if user is not None:
            login(request, user)
            response.set_cookie("user_id", user.user_id, max_age=3600 * 1)#最长登录时间1小时
            return response  # 重定向到登录后的页面
    return render(request, 'login.html')
def index(request):
    return render(request, "index.html")

def reg(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password_1 = request.POST.get('user_password_1')
        password_2 = request.POST.get('user_password_2')
        if not password_1 or not password_2:
            password_1_error = '请输入正确的密码'
            return render(request, 'login.html', locals())

        if password_1 != password_2:
            password_2_error = '两次密码不一致'
            return render(request, 'login.html', locals())

        try:
            old_user = User.objects.get(user_id=user_id)
            user_id_error = '用户已经被注册!'
            return render(request, 'login.html', locals())

        except Exception:

            try:
                user = User.objects.create(user_id=user_id, user_password=password_1)
                response = redirect("/index/")
                login(request, user)  # 注册后自动登录
                response.set_cookie("user_id", user.user_id, max_age=3600 * 1)  # 最长登录时间1小时
                return response  # 重定向到登录后的页面

            except Exception:#存在抢注可能
                user_id_error = '该用户名已经被占用'
                return render(request, 'login.html', locals())

    return render(request, 'login.html')
@login_required(login_url='/login/')
def personal(request):
    user = request.user
    if request.method == "POST":
            fields = user.fields
            form = UserForm(request.POST, request.FILES, instance=fields)
            if form.is_valid():
                form.save()
                return redirect('/personal/')
    else:
            fields = user.fields
            form = UserForm(instance=fields)
    return render(request, 'personal.html', locals())
def team_apply(request):
    return render(request, "team_apply.html")

def team_created(request):
    if(request.method=="GET"):
      return render(request, "team_created.html")


def team_join(request):
    return render(request, "team_join.html")
