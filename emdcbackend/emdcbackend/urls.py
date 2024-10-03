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
from .views.contest import contest_by_id, contest_get_all, create_contest, edit_contest, delete_contest
from .views.team import create_team, team_by_id, edit_team, delete_team_by_id
from .views.Maps.MapCoachToTeam import create_coach_team_mapping, coach_by_team_id, teams_by_coach_id
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
    path('getUser/<int:user_id>/', views.user_by_id),
    path('deleteUser/<int:user_id>/', views.delete_user_by_id),
    path('editUser/', views.edit_user),

    # Judges
    path('createJudge/', create_judge),
    path('getJudge/<int:judge_id>/', judge_by_id),
    path('editJudge/', edit_judge),
    path('deleteJudge/<int:judge_id>/', delete_judge),

    # Organizers
    path('createOrganizer/', create_organizer),
    path('getOrganizer/<int:organizer_id>/', organizer_by_id),
    path('editOrganizer', edit_organizer),
    path('deleteOrganizer/<int:organizer_id>/', delete_organizer),

    # Coaches
    path('getCoach/<int:coach_id>/', coach_by_id),
    path('createCoach/', create_coach),
    path('editCoach/', edit_coach),
    path('deleteCoach/<int:coach_id>/', delete_coach),
    path('getAllCoaches/', coach_get_all),
  
    # Teams
    path('getTeam/<int:team_id>/', team_by_id),
    path('createTeam/', create_team),
    path('editTeam/', edit_team),
    path('deleteTeam/<int:team_id>/', delete_team_by_id),

    # Maps
    path('mapCoachToTeam/', create_coach_team_mapping),
    path('getCoachByTeam/<int:team_id>/', coach_by_team_id),
    path('mapContestToJudge/',create_contest_judge_mapping),
    path('getJudgesByContest/<int:contest_id>/',get_all_judges_by_contest_id),
    path('getContestByJudge/<int:judge_id>/',get_contest_id_by_judge_id),
    path('mapContestToTeam/',create_contest_team_mapping),
    path('getTeamsByContest/<int:contest_id>/',get_teams_by_contest_id),
    path('getContestbyTeam/<int:team_id>/',get_contest_id_by_team_id),
    path('mapContestToOrganizer/',create_contest_organizer_mapping),
    path('getOrganizerByContest/<int:contest_id>/',get_organizers_by_contest_id),
    path('getContestsByOrganizer/<int:organizer_id>/',get_contests_by_organizer_id),
    path('getTeamsByCoach/<int:coach_id>/', teams_by_coach_id),

    # Clusters
    path('getCluster/<int:cluster_id>/', cluster_by_id),
    path('getAllClusters/', clusters_get_all),
    path('createCluster/', create_cluster),
    path('editCluster/', edit_cluster),
    path('deleteCluster/<int:cluster_id>/', delete_cluster),
    
    # Contests
    path('contestByID/<int:contest_id>/', contest_by_id),
    path('contestGetAll/',contest_get_all),
    path('createContest/',create_contest),
    path('editContest/',edit_contest),
    path('deleteContest/<int:contest_id>/',delete_contest),

    # Scoresheets
    path('createScoreSheet/',create_score_sheets),
    path('editScoreSheet/',edit_score_sheets),
    path('getScoreSheet/<int:scores_id>/',scores_by_id),
    path('deleteScoreSheet/<int:scores_id>/',delete_score_sheets),

    #Admins
    path('createAdmin/', create_admin),
    path('adminById/<int:admin_id>/', admin_by_id),
    path('allAdmins/', admins_get_all),
    path('deleteAdmin/<int:admin_id>/', delete_admin),
    path('editAdmin/', edit_admin),
  
    # Penalties
    path('createPenalties/',create_penalties),
    path('editPenalties/',edit_penalties),
    path('getPenalties/<int:penalties_id>/',penalties_by_id),
    path('deletePenalties/<int:penalties_id>/',delete_penalties)
]
