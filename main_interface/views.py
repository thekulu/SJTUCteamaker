from django.shortcuts import render, HttpResponse, redirect
from home_interface.models import User, Competition, Team, Discussion
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
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
    user = request.user
    if user.is_authenticated:
        user.is_authenticated = False
        user.save()
        return redirect('/index/')
        
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_password = request.POST.get('user_password')
        user_password_a = request.POST.get('user_password_a')
        # print("if",user_password_a)
        if user_password_a is not None:
            if user_password == user_password_a:
                new_user = User(
                    user_name="New User " + user_id,
                    user_id=user_id,  # 你需要选择一个唯一的学号
                    user_password=user_password,
                    profile="images/1成员1.jpeg",  # 上传的头像文件路径
                    bio="添加你的介绍",
                    major="添加你的专业"
                )
                new_user.save()
        
        user = authenticate(request, user_id=user_id, user_password=user_password)
        print(user)

        if user is not None:
            user.is_authenticated = True
            user.save()
            login(request, user)
            return redirect('/index/')  # 重定向到登录后的页面
    return render(request, 'login.html')

def personal_add(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        try:
            user_name = request.POST.get('user_name')
            # user_password = request.POST.get('user_password')
            # user_id = request.POST.get('user_id')
            user_grade = request.POST.get('grade')
            user_email = request.POST.get('email')
            major = request.POST.get('major')
            bio = request.POST.get('bio')
            profile = request.FILES.get('profile')  # 头像文件

            if profile:
                print("change")
                # 保存文件到media目录中
                file_name = default_storage.save('profile_pictures/' + profile.name, ContentFile(profile.read()))

                # 获取文件的URL
                file_url = 'profile_pictures/' + profile.name
            else:
                file_url = user.profile

            # 创建用户并保存到数据库
        
            user.user_name=user_name
            user.user_grade=user_grade
            user.user_email=user_email
            user.major=major
            user.profile=file_url
            user.bio=bio
        except:
            messages.error(request, '请正确输入')

        user.save()

        # print(user.user_grade,user.user_email)
        return redirect('/personal/')  # 重定向到用户个人资料页面或其他页面


# Create your views here.
def index(request):
    return render(request, "index.html")

# @login_required(login_url='/login')

def personal(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
    return render(request, 'personal.html', {'user': user})

def team_apply(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
    competition = Competition.objects.filter(name = input)
    return render(request, 'team_apply.html', {'user': user})

def team_created(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
    team = Team.objects.filter(creator = user)
    return render(request, 'team_created.html', {'user': user, 'team': team})

def team_join(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
    team = Team.objects.filter(members = user)
    return render(request, 'team_join.html', {'user': user, 'team': team})