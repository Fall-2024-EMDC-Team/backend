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
from django.urls import path
from .auth import views
from .views.judge import create_judge, judge_by_id, edit_judge, delete_judge
from .views.organizer import create_organizer, organizer_by_id, edit_organizer, delete_organizer
from .views.coach import create_coach, coach_by_id, edit_coach, delete_coach, coach_get_all
from .views.contest import contest_by_id, contest_get_all, create_contest, edit_contest, delete_contest
from .views.team import create_team, team_by_id, edit_team, delete_team_by_id
from .views.Maps.MapCoachToTeam import create_coach_team_mapping, coach_by_team_id
from .views.clusters import cluster_by_id, create_cluster, clusters_get_all, delete_cluster, edit_cluster
from .views.Maps.MapContestToJudge import create_contest_judge_mapping, get_all_judges_by_contest_id, get_contest_id_by_judge_id
from .views.Maps.MapContestToOrganizer import create_contest_organizer_mapping, get_organizers_by_contest_id, get_contests_by_organizer_id
from .views.Maps.MapContestToTeam import create_contest_team_mapping, get_teams_by_contest_id, get_contest_id_by_team_id
from .views.scoresheets import create_score_sheets, edit_score_sheets, scores_by_id, delete_score_sheets
from .views.admin import create_admin, admins_get_all, admin_by_id, delete_admin, edit_admin
from .views.penalties import penalties_by_id, create_penalties, edit_penalties, delete_penalties

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('login/', views.login),
    path('signup/', views.signup),
    path('testToken/', views.test_token),

    # Users
    path('user/get/<int:user_id>/', views.user_by_id),
    path('user/edit/', views.edit_user),
    path('user/delete/<int:user_id>/', views.delete_user_by_id),

    # Judges
    path('judge/get/<int:judge_id>/', judge_by_id),
    path('judge/create/', create_judge),
    path('judge/edit/', edit_judge),
    path('judge/delete/<int:judge_id>/', delete_judge),

    # Organizers
    path('organizer/get/<int:organizer_id>/', organizer_by_id),
    path('organizer/create/', create_organizer),
    path('organizer/edit/', edit_organizer),
    path('organizer/delete/<int:organizer_id>/', delete_organizer),

    # Coaches
    path('coach/get/<int:coach_id>/', coach_by_id),
    path('coach/getall/', coach_get_all),
    path('coach/create/', create_coach),
    path('coach/edit/', edit_coach),
    path('coach/delete/<int:coach_id>/', delete_coach),
  
    # Teams
    path('team/get/<int:team_id>/', team_by_id),
    path('team/create/', create_team),
    path('team/edit/', edit_team),
    path('team/delete/<int:team_id>/', delete_team_by_id),

    # Maps
    path('coach/toTeam/map/', create_coach_team_mapping),
    path('coach/toTeam/get/<int:team_id>/', coach_by_team_id),
    path('contest/toJudge/map/',create_contest_judge_mapping),
    path('contest/toTeam/get/<int:team_id>/',get_contest_id_by_team_id),
    path('contest/toOrganizer/map/',create_contest_organizer_mapping),
    path('contest/toJudge/get/<int:judge_id>/',get_contest_id_by_judge_id),
    path('contest/toTeam/map/',create_contest_team_mapping),
    path('contest/toOrganizer/get/<int:organizer_id>/',get_contests_by_organizer_id),
    path('judge/toContest/get/<int:contest_id>/',get_all_judges_by_contest_id),
    path('team/toContest/get/<int:contest_id>/',get_teams_by_contest_id),
    path('organizer/toContest/get/<int:contest_id>/',get_organizers_by_contest_id),

    # Clusters
    path('cluster/get/<int:cluster_id>/', cluster_by_id),
    path('cluster/getall/', clusters_get_all),
    path('cluster/create/', create_cluster),
    path('cluster/edit/', edit_cluster),
    path('cluster/delete/<int:cluster_id>/', delete_cluster),
    
    # Contests
    path('contest/get/<int:contest_id>/', contest_by_id),
    path('contest/getall/',contest_get_all),
    path('contest/create/',create_contest),
    path('contest/edit/',edit_contest),
    path('contet/delete/<int:contest_id>/',delete_contest),

    # Scoresheets
    path('schoresheet/get/<int:scores_id>/',scores_by_id),
    path('scoresheet/create/',create_score_sheets),
    path('scoresheet/edit/',edit_score_sheets),
    path('schoresheet/delete/<int:scores_id>/',delete_score_sheets),

    #Admins
    path('admin/get/<int:admin_id>/', admin_by_id),
    path('admin/getall/', admins_get_all),
    path('admin/create/', create_admin),
    path('admin/edit/', edit_admin),
    path('admin/delete/<int:admin_id>/', delete_admin),
  
    # Penalties
    path('penalties/get/<int:penalties_id>/',penalties_by_id),
    path('penalites/create/',create_penalties),
    path('penalties/edit/',edit_penalties),
    path('penalties/delete/<int:penalties_id>/',delete_penalties)
]
