from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import render, get_object_or_404
from .models import User, Competition, Team

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
    return render(request, "blog.html")

def blogs(request):
    competition = Competition.objects.first()
    return render(request, 'blog-single.html', {'competition': competition})

# def blogs(request):
#     new_competition = Competition(
#         name="Competition 0 from sql",
#         start_date="2023-11-01",
#         end_date="2023-11-27",
#         description="Description of the new competition1."
#     )
#     new_competition.save()
#     return render(request, 'blog-single.html', {'competition': new_competition})