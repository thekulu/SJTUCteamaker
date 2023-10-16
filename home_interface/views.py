from django.shortcuts import render, HttpResponse, redirect




# Create your views here.
def home(request):
    return render(request, "home.html")

def blog(request):
    return render(request, "blog.html")

def blogs(request):
    return render(request, "blog-single.html")