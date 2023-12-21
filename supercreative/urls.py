"""
URL configuration for supercreative project.

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
from django.contrib import admin
from django.urls import path
from supercreative.views import Login, Test, Courses, Home, Users, ManageCourse, UserPage
from supercreative import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('test/', Test.as_view()),
    path('users/', Users.as_view()),
    path('course/', Courses.as_view()),
    path('manage-course/', ManageCourse.as_view()),
    path('account/', UserPage.as_view()),
    path('home/', Home.as_view()),
    path('course/nonexistantcourse/', Courses.as_view()),
    path('', Login.as_view()),
]
