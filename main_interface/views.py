from django.shortcuts import render, HttpResponse, redirect


# Create your views here.
def index(request):
    return render(request, "index.html")

def personal(request):
    return render(request, "personal.html")

def team_apply(request):
    return render(request, "team_apply.html")

def team_created(request):
    return render(request, "team_created.html")

def team_join(request):
    return render(request, "team_join.html")