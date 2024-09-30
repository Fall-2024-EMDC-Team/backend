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
from .views.organizer import create_organizer, organizer_by_id, edit_organizer, delete_organizer
from .views.coach import create_coach, coach_by_id, edit_coach, delete_coach, coach_get_all
from .views.Maps.MapCoachToTeam import create_coach_team_mapping, coach_by_team_id
from .views.clusters import cluster_by_id, create_cluster, clusters_get_all, delete_cluster, edit_cluster

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
    path('createOrganizer/', create_organizer),
    path('getOrganizer/<int:organizer_id>/', organizer_by_id),
    path('editOrganizer', edit_organizer),
    path('deleteOrganizer/<int:organizer_id>/', delete_organizer),
    path('getCoach/<int:coach_id>/', coach_by_id),
    path('createCoach/', create_coach),
    path('editCoach/', edit_coach),
    path('deleteCoach/<int:coach_id>/', delete_coach),
    path('getAllCoaches/', coach_get_all),
    path('mapCoachToTeam/', create_coach_team_mapping),
    path('getCoachByTeam/<int:team_id>/', coach_by_team_id),
    path('getCluster/<int:cluster_id>/', cluster_by_id),
    path('getAllClusters/', clusters_get_all),
    path('createCluster/', create_cluster),
    path('editCluster/', edit_cluster),
    path('deleteCluster/<int:cluster_id>/', delete_cluster)
]
