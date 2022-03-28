"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from exam import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),  # 默认访问首页
    url('index/', views.index, name='index'),
    url('user_login/', views.user_login, name='user_login'),                # 用户登录
    url('start_exam/', views.start_exam, name='start_exam'),                # 开始考试
    url('calculate_grade/', views.calculate_grade, name='calculate_grade'),  # 考试评分
    path('user_logout/', views.user_logout, name='user_logout'),            # 学生退出登录
    path('user_file/', views.user_file, name='user_file'),                  # 用户的个人信息
    path('user_exam/', views.user_exam, name='user_exam'),                  # 考试信息
    path('exam_info/', views.exam_info, name='exam_info')                   # 考试成绩
]
