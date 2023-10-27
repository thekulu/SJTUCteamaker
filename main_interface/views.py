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
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        user_id = request.POST.get('user_id')
        user_grade = request.POST.get('user_grade')
        user_email = request.POST.get('user_email')
        profile = request.FILES.get('profile')  # 头像文件

        if profile:
            # 保存文件到media目录中
            file_name = default_storage.save('profile_pictures/' + profile.name, ContentFile(profile.read()))

            # 获取文件的URL
            file_url = 'profile_pictures/' + profile.name

        # 创建用户并保存到数据库
        user = User(
            user_name=user_name,
            user_password=user_password,
            user_id=user_id,
            user_grade=user_grade,
            user_email=user_email,
            profile=file_url  # 上传的头像
        )
        user.save()

        # 设置用户已认证为 True
        user.is_authenticated = True
        user.save()

        messages.success(request, '用户添加成功')
        return redirect('/personal/')  # 重定向到用户个人资料页面或其他页面
    
def personal_add(request):
    # 默认为 POST 表单    
    name = request.POST.get("name")
    url = request.POST.get("url")
    inputfile = request.FILES.get('inputfile')
    number = request.POST.get("number")
    
    # 竞赛类别单选项
    category = request.POST.get("category")

    start_regi = request.POST.get("start_regi")
    end_regi = request.POST.get("end_regi")
    start_compt = request.POST.get("start_compt")
    intro = request.POST.get("intro")

    # 处理上传的文件
    if inputfile:
        # 保存文件到media目录中
        file_name = default_storage.save('profile_pictures/' + inputfile.name, ContentFile(inputfile.read()))

        # 获取文件的URL
        file_url = 'profile_pictures/' + inputfile.name

    Competition.objects.create(name = name,
                                url = url, 
                                image = file_url,
                                number = number,
                                category = category,
                                start_regi = start_regi,
                                end_regi = end_regi,
                                start_compt = start_compt,
                                intro = intro
                                )
    # return HttpResponse("添加成功")
    messages.error(request, '添加成功')
    return redirect("/personel/") # urls.py 中的 personel.html 地址

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