"""
URL configuration for TeamProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import main, anime_details, anime_watching, blog, blog_details, categories, login, signup

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),

    path('anime_details', anime_details, name='anime_details'),

    path('anime_watching', anime_watching, name='anime_watching'),

    path('blog', blog, name='blog'),

    path('blog_details', blog_details, name='blog_details'),

    path('categories', categories, name='categories'),

    path('login', login, name='login'),

    path('signup', signup, name='signup'),
]
