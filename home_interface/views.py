from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import render, get_object_or_404
from .models import User, Competition, Team, Discussion

def new_competition():
    new_competition = Competition(
        name="Competition 1 from sql",
        start_date="2023-11-01",
        end_date="2023-11-30",
        description="Description of the new competition."
    )
    new_competition.save()

# Create your views here.
def home(request):
    return render(request, "home.html")

def blog(request):
    competition = Competition.objects.all()  # 查询数据库中的所有Discussion对象
    return render(request, "blog.html",  {'competition': competition})

def blogs(request, competition_id):
    if request.method == 'POST':
        # 获取当前登录用户
        # user = request.user
        user = User.objects.first()
        competition = Competition.objects.get(pk=competition_id)

        # 获取POST数据
        content = request.POST.get('comment')

        # 检查 content 是否存在
        if content:
            # 创建 Discussion 对象并将其保存到数据库
            new_discussion = Discussion(content=content, user=user, competition=competition)
            new_discussion.save()

            # 返回响应，可以是重定向或其他响应
            return HttpResponse('讨论已发布')
    # 获取所有Discussion对象
    competition = Competition.objects.get(pk=competition_id)
    teams = Team.objects.filter(competition=competition)
    discussions = Discussion.objects.filter(competition=competition)
    return render(request, 'blog-single.html', {'competition': competition, 'discussions': discussions, 'teams': teams})

    
# def blogs(request, competition_id):
#     # 创建一个新的 User 实例
#     new_user = User(
#         user_name="Bob",
#         user_id=2,  # 你需要选择一个唯一的学号
#         user_password="2003",
#         profile="profile_picture.jpg",  # 上传的头像文件路径
#         bio="Self-introduction",
#         major="Computer Science"
#     )

#     # 保存该实例到数据库
#     new_user.save()
#     # 创建一个新的 Competition 实例
#     new_competition = Competition(
#         name="“挑战杯” 全国大学生课外学术科技作品竞赛",
#         image="img/blog/blog-1.jpg",  # 上传的竞赛图片文件路径
#         start_regi="2023-11-01",
#         end_regi="2023-11-25",
#         start_compt="2023-11-30",
#         url="https://tiaozhanbei.com",
#         number=100,
#         intro="“挑战杯” 系列竞赛被誉为中国大学生学术科技 “奥林匹克” ，是国内大学生最关注最热门的全国性竞赛，也是全国最具代表性、权威性、示范性、导向性的大学生竞赛。该竞赛每两年举办一次，旨在鼓励大学生勇于创新、迎接挑战的精神，培养跨世纪创新人才。",
#         category=1  # 使用合适的类别值
#     )

#     # 保存该实例到数据库
#     new_competition.save()
#     # 创建一个新的 Team 实例
#     new_team = Team(
#         name="开心超人队",
#         competition=new_competition,  # 将团队与特定竞赛相关联
#         creator=new_user,  # 将团队的创建者设置为特定用户
#     )

#     # 保存该实例到数据库
#     new_team.save()
#     # 创建一个新的 Discussion 实例
#     new_discussion = Discussion(
#         content="good good",
#         user=new_user,  # 将讨论与特定用户相关联
#         competition=new_competition,  # 将讨论与特定竞赛相关联
#     )
#     # 保存该实例到数据库
#     new_discussion.save()
#     return render(request, 'blog-single.html', {'competition': new_competition, 'discussions': new_discussion, 'teams': new_team})