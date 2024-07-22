# Create your views here.
from django.shortcuts import render


def main(request):
    return render(request, 'index.html')


def anime_details(request):
    return render(request, 'anime-details.html')


def anime_watching(request):
    return render(request, 'anime-watching.html')


def blog(request):
    return render(request, 'blog.html')


def blog_details(request):
    return render(request, 'blog-details.html')


def categories(request):
    return render(request, 'categories.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
