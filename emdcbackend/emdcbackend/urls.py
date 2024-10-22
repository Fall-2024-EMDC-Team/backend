from django.urls import path
from .auth import views
from .views.Maps.MapClusterToTeam import create_cluster_team_mapping, delete_cluster_team_mapping_by_id, \
    teams_by_cluster_id, cluster_by_team_id
from .views.Maps.MapScoreSheet import create_score_sheet_mapping, score_sheets_by_judge_team, \
    delete_score_sheet_mapping_by_id
from .views.judge import create_judge, judge_by_id, edit_judge, delete_judge
from .views.organizer import create_organizer, organizer_by_id, edit_organizer, delete_organizer
from .views.coach import create_coach, coach_by_id, edit_coach, delete_coach, coach_get_all
from .views.contest import contest_by_id, contest_get_all, create_contest, edit_contest, delete_contest
from .views.team import create_team, team_by_id, edit_team, delete_team_by_id
from .views.Maps.MapCoachToTeam import create_coach_team_mapping, coach_by_team_id, delete_coach_team_mapping_by_id, teams_by_coach_id
from .views.clusters import cluster_by_id, create_cluster, clusters_get_all, delete_cluster, edit_cluster
from .views.Maps.MapContestToJudge import create_contest_judge_mapping, get_all_judges_by_contest_id, get_contest_id_by_judge_id, delete_contest_judge_mapping_by_id
from .views.Maps.MapContestToOrganizer import create_contest_organizer_mapping, get_organizers_by_contest_id, get_contests_by_organizer_id, delete_contest_organizer_mapping_by_id
from .views.Maps.MapContestToTeam import create_contest_team_mapping, get_teams_by_contest_id, get_contest_id_by_team_id, delete_contest_team_mapping_by_id
from .views.scoresheets import create_score_sheet, edit_score_sheet, scores_by_id, delete_score_sheet
from .views.admin import create_admin, admins_get_all, admin_by_id, delete_admin, edit_admin
from .views.Maps.MapUserToRole import create_user_role_mapping, delete_user_role_mapping
from .views.Maps.MapClusterToJudge import create_cluster_judge_mapping, delete_cluster_judge_mapping_by_id, cluster_by_judge_id, judges_by_cluster_id

urlpatterns = [
    # Admins
    path('admin/get/<int:admin_id>/', admin_by_id, name='admin_by_id'),
    path('admin/getAll/', admins_get_all, name='admins_get_all'),
    path('admin/create/', create_admin, name='create_admin'),
    path('admin/edit/', edit_admin, name='edit_admin'),
    path('admin/delete/<int:admin_id>/', delete_admin, name='delete_admin'),

    # Authentication
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('testToken/', views.test_token, name='test_token'),

    # Users
    path('user/get/<int:user_id>/', views.user_by_id, name='user_by_id'),
    path('user/edit/', views.edit_user, name='edit_user'),
    path('user/delete/<int:user_id>/', views.delete_user_by_id, name='delete_user_by_id'),

    # Judges
    path('judge/get/<int:judge_id>/', judge_by_id, name='judge_by_id'),
    path('judge/create/', create_judge, name='create_judge'),
    path('judge/edit/', edit_judge, name='edit_judge'),
    path('judge/delete/<int:judge_id>/', delete_judge, name='delete_judge'),

    # Organizers
    path('organizer/get/<int:organizer_id>/', organizer_by_id, name='organizer_by_id'),
    path('organizer/create/', create_organizer, name='create_organizer'),
    path('organizer/edit/', edit_organizer, name='edit_organizer'),
    path('organizer/delete/<int:organizer_id>/', delete_organizer, name='delete_organizer'),

    # Coaches
    path('coach/get/<int:coach_id>/', coach_by_id, name='coach_by_id'),
    path('coach/getAll/', coach_get_all, name='coach_get_all'),
    path('coach/create/', create_coach, name='create_coach'),
    path('coach/edit/', edit_coach, name='edit_coach'),
    path('coach/delete/<int:coach_id>/', delete_coach, name='delete_coach'),

    # Teams
    path('team/get/<int:team_id>/', team_by_id, name='team_by_id'),
    path('team/create/', create_team, name='create_team'),
    path('team/edit/', edit_team, name='edit_team'),
    path('team/delete/<int:team_id>/', delete_team_by_id, name='delete_team_by_id'),

    # Maps
    path('mapping/coachToTeam/create/', create_coach_team_mapping, name='create_coach_team_mapping'),
    path('mapping/coachToTeam/getCoachByTeam/<int:team_id>/', coach_by_team_id, name='coach_by_team_id'),
    path('mapping/coachToTeam/delete/<int:map_id>/', delete_coach_team_mapping_by_id, name='delete_coach_team_mapping'),
    path('api/coachToTeam/teamsByCoach/<int:coach_id>/', teams_by_coach_id, name='teams_by_coach_id'),

    path('mapping/contestToJudge/create/', create_contest_judge_mapping, name='create_contest_judge_mapping'),
    path('mapping/contestToJudge/getContestByJudge/<int:judge_id>/', get_contest_id_by_judge_id, name='get_contest_id_by_judge_id'),
    path('mapping/contestToJudge/delete/<int:map_id>/', delete_contest_judge_mapping_by_id, name='delete_contest_judge_mapping'),

    path('mapping/contestToTeam/create/', create_contest_team_mapping, name='create_contest_team_mapping'),
    path('mapping/contestToTeam/getContestByTeam/<int:team_id>/', get_contest_id_by_team_id, name='get_contest_id_by_team_id'),
    path('mapping/contestToTeam/delete/<int:map_id>/', delete_contest_team_mapping_by_id, name='delete_contest_team_mapping'),

    path('mapping/contestToOrganizer/create/', create_contest_organizer_mapping, name='create_contest_organizer_mapping'),
    path('mapping/contestToOrganizer/getByOrganizer/<int:organizer_id>/', get_contests_by_organizer_id, name='get_contests_by_organizer_id'),
    path('mapping/contestToOrganizer/delete/<int:map_id>/', delete_contest_organizer_mapping_by_id, name='delete_contest_organizer_mapping'),

    path('mapping/judgeToContest/getAllJudges/<int:contest_id>/', get_all_judges_by_contest_id, name='get_all_judges_by_contest_id'),
    path('mapping/teamToContest/getTeamsByContest/<int:contest_id>/', get_teams_by_contest_id, name='get_teams_by_contest_id'),
    path('mapping/organizerToContest/getOrganizersByContest/<int:contest_id>/', get_organizers_by_contest_id, name='get_organizers_by_contest_id'),

    path('mapping/userToRole/create/', create_user_role_mapping, name='create_user_role_mapping'),
    path('mapping/userToRole/delete/<int:mapping_id>/', delete_user_role_mapping, name='delete_user_role_mapping'),

    path('mapping/clusterToTeam/create/', create_cluster_team_mapping, name='create_cluster_team_mapping'),
    path('mapping/clusterToTeam/delete/<int:map_id>/', delete_cluster_team_mapping_by_id, name='delete_cluster_team_mapping'),
    path('mapping/clusterToTeam/getAllTeamsByCluster/<int:cluster_id>/', teams_by_cluster_id, name='teams_by_cluster'),
    path('mapping/clusterToTeam/getClusterByTeam/<int:team_id>/', cluster_by_team_id, name='cluster_by_team'),

    path('mapping/clusterToJudge/create/', create_cluster_judge_mapping, name='create_cluster_judge_mapping'),
    path('mapping/clusterToJudge/delete/<int:map_id>/', delete_cluster_judge_mapping_by_id, name='delete_cluster_judge_mapping'),
    path('mapping/clusterToJudge/getAllJudgesByCluster/<int:cluster_id>/', judges_by_cluster_id, name='judges_by_cluster'),
    path('mapping/clusterToJudge/getClusterByJudge/<int:judge_id>/', cluster_by_judge_id, name='cluster_by_judge'),

    path('mapping/scoreSheet/create/', create_score_sheet_mapping, name='create_score_sheet_mapping'),
    path('mapping/scoreSheet/getByTeamJudge/<int:judge_id>/<int:team_id>/', score_sheets_by_judge_team, name='score_sheets_by_judge_team'),
    path('mapping/scoreSheet/delete/', delete_score_sheet_mapping_by_id, name='delete_score_sheet_mapping_by_id'),

    # Clusters
    path('cluster/get/<int:cluster_id>/', cluster_by_id, name='cluster_by_id'),
    path('cluster/getAll/', clusters_get_all, name='clusters_get_all'),
    path('cluster/create/', create_cluster, name='create_cluster'),
    path('cluster/edit/', edit_cluster, name='edit_cluster'),
    path('cluster/delete/<int:cluster_id>/', delete_cluster, name='delete_cluster'),

    # Contests
    path('contest/get/<int:contest_id>/', contest_by_id, name='contest_by_id'),
    path('contest/getAll/', contest_get_all, name='contest_get_all'),
    path('contest/create/', create_contest, name='create_contest'),
    path('contest/edit/', edit_contest, name='edit_contest'),
    path('contest/delete/<int:contest_id>/', delete_contest, name='delete_contest'),

    # ScoreSheets
    path('scoreSheet/get/<int:scores_id>/', scores_by_id, name='scores_by_id'),
    path('scoreSheet/create/', create_score_sheet, name='create_score_sheets'),
    path('scoreSheet/edit/', edit_score_sheet, name='edit_score_sheets'),
    path('scoreSheet/delete/<int:scores_id>/', delete_score_sheet, name='delete_score_sheets'),

]
