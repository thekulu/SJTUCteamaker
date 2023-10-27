from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    user_name = models.CharField(max_length=15)
    user_id = models.IntegerField(validators=[MaxValueValidator(20), MinValueValidator(1)], unique=True) #学号
    user_password = models.CharField(max_length=20)
    #profile = models.ImageField(upload_to='profile_pictures/', null=True, blank=True) #头像

    bio = models.TextField(max_length=500, blank=True,null=True) #Self-introduction
    major = models.CharField(max_length=100)
    last_login = models.DateTimeField( auto_now = True)
    def __str__(self):
        return self.user_name

class Competition(models.Model):

    CATEGORY_CHOICES = [(1, 'Category 1'), (2, 'Category 2'), (3, 'Category 3')]

    name = models.CharField(max_length=100,unique=True)
    #image = models.ImageField(upload_to='competition_images/', null=True, blank=True) #相关图片

    start_regi = models.DateField()  #报名开始时间
    end_regi = models.DateField()    #报名截止时间
    start_compt = models.DateField() #竞赛开始时间

    url = models.URLField(max_length=200, null=True, blank=True) #来源网站
    number = models.PositiveIntegerField(null=True, blank=True) #参赛人数
    intro = models.TextField() # 竞赛简介

    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)  #竞赛类别


    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='joined_teams')
    created = models.DateTimeField(auto_now_add=True) #创建时间
    updated = models.DateTimeField(auto_now=True)     #更新时间

    def __str__(self):
        return self.name

class Discussion(models.Model):
    content = models.TextField()  #讨论内容
    discuss_time = models.DateTimeField(auto_now_add=True)  #发布时间
    updated = models.DateTimeField(auto_now=True)           #更新时间
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')

    def __str__(self):
        return self.content[:20]