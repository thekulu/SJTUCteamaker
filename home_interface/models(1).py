from django.db import models

# Create your models here

class User(models.Model):
    user_name = models.CharField(max_length=15)
    user_id = models.IntegerField(max_digits=15,unique=True)#学号
    user_password = models.CharField(max_length=20)
    bio = models.TextField(max_length=500, blank=True)#Self-introduction
    major = models.CharField(max_length=100)
    profile=models.ImageField(upload_to='profile_pictures/', null=True, blank=True)#头像
    def __str__(self):
        return self.user_name

class Competition(models.Model):
    name = models.CharField(max_length=100,unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='joined_teams')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):

    team = models.ForeignKey(Team, on_delete=models.CASCADE,null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
