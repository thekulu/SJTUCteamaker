from django.shortcuts import render, HttpResponse, redirect




# Create your views here.
def index(request):
    return render(request, "index.html")

def blog(request):
    return render(request, "blog.html")

def blogs(request):
    return render(request, "blog-single.html")