"""
URL configuration for emdcbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from .auth import views
from .views.judge import create_judge, judge_by_id, edit_judge, delete_judge
from .views.team import team_by_id, create_team, edit_team, delete_team_by_id

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('signup/', views.signup),
    path('testToken/', views.test_token),
    path('getUser/<int:user_id>/', views.user_by_id),
    path('deleteUser/<int:user_id>/', views.delete_user_by_id),
    path('editUser/', views.edit_user),
    path('createJudge/', create_judge),
    path('getJudge/<int:judge_id>/', judge_by_id),
    path('editJudge/', edit_judge),
    path('deleteJudge/<int:judge_id>/', delete_judge),

    path('getTeam/<int:judge_id>/', team_by_id),
    path('createTeam/', create_team),
    path('editTeam/', edit_team),
    path('deleteTeam/<int:judge_id>/', delete_team_by_id)
]
