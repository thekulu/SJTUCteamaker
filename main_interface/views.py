from django.shortcuts import render, HttpResponse, redirect
from home_interface.models import User, Competition, Team, Notification, TeamApplication
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.db.models import Q
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
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        response = request.POST.get('response')
        respond_to_application(request, application_id, response)
        return redirect('/team_apply/')
    if not user.is_authenticated:
        return redirect('/login/')
    team = Team.objects.filter(creator = user)
    if team:
        application_o = TeamApplication.objects.filter(Q(status='Pending') & Q(team__in=team))
        print(application_o)
    else:
        application_o = None
    application_i = TeamApplication.objects.filter(applicant = user, status = 'Pending')
    # notification = Notification.objects.filter(recipient = user, is_read = False)
    return render(request, 'team_apply.html', {'user': user, 'application_o': application_o, 'application_i': application_i})

def team_created(request):
    user = request.user
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        team = Team.objects.get(pk=team_id)
        applications = TeamApplication.objects.filter(team=team)

        # 遍历每个申请
        if applications:
            for application in applications:
                # 创建通知
                Notification.objects.create(
                    recipient=application.applicant,
                    content=f"你的申请加入队伍 {application.team.name} 已经被解散.",
                    related_application=application
                )
                # 删除申请
                application.delete()

        team.delete()
        
    if not user.is_authenticated:
        return redirect('/login/')
    team = Team.objects.filter(creator = user)
    return render(request, 'team_created.html', {'user': user, 'team': team})

def team_join(request):
    user = request.user
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        team = Team.objects.get(pk=team_id)
        # 创建通知
        Notification.objects.create(
            recipient=team.creator,
            content=f"你的队伍 {team.name} 内的组员{user.user_name}已经退出.",
            related_application=None
        )
        team.members.remove(user)
        team.save()
        return redirect('/team_join/')
    team = Team.objects.filter(members = user)
    return render(request, 'team_join.html', {'user': user, 'team': team})

def notification(request):
    user = request.user
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        Notification.objects.get(pk = notification_id).delete()
        return redirect('/notification/')
    notification = Notification.objects.filter(recipient = user)
    return render(request, 'notification.html', {'user': user, 'notification': notification})


#队长做出决定后生成信息
def respond_to_application(request, application_id, response):
    application = TeamApplication.objects.get(pk=application_id)

    if response == "accept":
        application.status = "accepted"
        application.save()
        add_member_to_team(application) #加入到队伍

        #生成同意的Notification
        Notification.objects.create(
            recipient=application.applicant,
            content=f"你申请加入队伍 {application.team.name} 已经被同意",
            related_application=application
        )
        #生成拒绝的Notification
    elif response == "reject":
        application.status = "rejected"
        application.save()
        Notification.objects.create(
            recipient=application.applicant,
            content=f"你申请加入队伍 {application.team.name} 已经被拒绝.",
            related_application=application
        )
    elif response == "delete":
        Notification.objects.create(
            recipient=application.applicant,
            content=f"你申请加入队伍 {application.team.name} 已经被你自己删除.",
            related_application=application
        )
        application.delete()
    return

#把申请者加入队伍
def add_member_to_team(application):
    if application.status == "accepted":
        application.team.members.add(application.applicant)
        application.team.save()