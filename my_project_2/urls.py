"""
URL configuration for my_project_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
    # Главная страница
    path('index.html', views.index, name='index'),
    path('', views.index),  # корневой URL тоже ведет на главную
    
    # Список курсов
    path('courses.html', views.courses, name='courses'),
    
    # Страница конкретного курса (с параметром course_id)
    path('course_<int:course_id>.html', views.course_detail, name='course_detail'),
    
    # Список авторов
    path('authors.html', views.authors, name='authors'),
    
    # Страница конкретного автора (с параметром author_id)
    path('author_<int:author_id>.html', views.author_detail, name='author_detail'),
    
    # Информационная страница
    path('info.html', views.info, name='info'),
]
