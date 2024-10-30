from django.urls import path
from .auth import views
from .views.Maps.MapClusterToContest import all_clusters_by_contest_id
from .views.Maps.MapClusterToTeam import create_cluster_team_mapping, delete_cluster_team_mapping_by_id, \
    teams_by_cluster_id, cluster_by_team_id
from .views.Maps.MapScoreSheet import create_score_sheet_mapping, score_sheet_by_judge_team, \
    delete_score_sheet_mapping_by_id
from .views.judge import create_judge, judge_by_id, edit_judge, delete_judge, are_all_score_sheets_submitted
from .views.organizer import create_organizer, organizer_by_id, edit_organizer, delete_organizer
from .views.coach import create_coach, coach_by_id, edit_coach, delete_coach, coach_get_all
from .views.contest import contest_by_id, contest_get_all, create_contest, edit_contest, delete_contest
from .views.team import create_team, team_by_id, edit_team, delete_team_by_id
from .views.Maps.MapCoachToTeam import create_coach_team_mapping, coach_by_team_id, delete_coach_team_mapping_by_id, teams_by_coach_id
from .views.clusters import cluster_by_id, create_cluster, clusters_get_all, delete_cluster, edit_cluster
from .views.Maps.MapContestToJudge import create_contest_judge_mapping, get_all_judges_by_contest_id, get_contest_id_by_judge_id, delete_contest_judge_mapping_by_id
from .views.Maps.MapContestToOrganizer import create_contest_organizer_mapping, get_organizers_by_contest_id, get_contests_by_organizer_id, delete_contest_organizer_mapping_by_id
from .views.Maps.MapContestToTeam import create_contest_team_mapping, get_teams_by_contest_id, get_contest_id_by_team_id, delete_contest_team_mapping_by_id
from .views.scoresheets import create_score_sheet, edit_score_sheet, scores_by_id, delete_score_sheet, \
    edit_score_sheet_field, update_scores
from .views.admin import create_admin, admins_get_all, admin_by_id, delete_admin, edit_admin
from .views.Maps.MapUserToRole import create_user_role_mapping, delete_user_role_mapping, get_user_by_role
from .views.Maps.MapClusterToJudge import create_cluster_judge_mapping, delete_cluster_judge_mapping_by_id, cluster_by_judge_id, judges_by_cluster_id
from .views.tabulation import tabulate_scores

urlpatterns = [
    # Admins
    path('api/admin/get/<int:admin_id>/', admin_by_id, name='admin_by_id'),
    path('api/admin/getAll/', admins_get_all, name='admins_get_all'),
    path('api/admin/create/', create_admin, name='create_admin'),
    path('api/admin/edit/', edit_admin, name='edit_admin'),
    path('api/admin/delete/<int:admin_id>/', delete_admin, name='delete_admin'),

    # Authentication
    path('api/login/', views.login, name='login'),
    path('api/signup/', views.signup, name='signup'),
    path('api/testToken/', views.test_token, name='test_token'),

    # Users
    path('api/user/get/<int:user_id>/', views.user_by_id, name='user_by_id'),
    path('api/user/edit/', views.edit_user, name='edit_user'),
    path('api/user/delete/<int:user_id>/', views.delete_user_by_id, name='delete_user_by_id'),

    # Judges
    path('api/judge/get/<int:judge_id>/', judge_by_id, name='judge_by_id'),
    path('api/judge/create/', create_judge, name='create_judge'),
    path('api/judge/edit/', edit_judge, name='edit_judge'),
    path('api/judge/delete/<int:judge_id>/', delete_judge, name='delete_judge'),
    path('api/judge/allScoreSheetsSubmitted/', are_all_score_sheets_submitted, name='are_all_score_sheets_submitted'),

    # Organizers
    path('api/organizer/get/<int:organizer_id>/', organizer_by_id, name='organizer_by_id'),
    path('api/organizer/create/', create_organizer, name='create_organizer'),
    path('api/organizer/edit/', edit_organizer, name='edit_organizer'),
    path('api/organizer/delete/<int:organizer_id>/', delete_organizer, name='delete_organizer'),

    # Coaches
    path('api/coach/get/<int:coach_id>/', coach_by_id, name='coach_by_id'),
    path('api/coach/getAll/', coach_get_all, name='coach_get_all'),
    path('api/coach/create/', create_coach, name='create_coach'),
    path('api/coach/edit/', edit_coach, name='edit_coach'),
    path('api/coach/delete/<int:coach_id>/', delete_coach, name='delete_coach'),

    # Teams
    path('api/team/get/<int:team_id>/', team_by_id, name='team_by_id'),
    path('api/team/create/', create_team, name='create_team'),
    path('api/team/edit/', edit_team, name='edit_team'),
    path('api/team/delete/<int:team_id>/', delete_team_by_id, name='delete_team_by_id'),

    # Maps

    path('api/mapping/coachToTeam/create/', create_coach_team_mapping, name='create_coach_team_mapping'),
    path('api/mapping/coachToTeam/getCoachByTeam/<int:team_id>/', coach_by_team_id, name='coach_by_team_id'),
    path('api/mapping/coachToTeam/delete/<int:map_id>/', delete_coach_team_mapping_by_id, name='delete_coach_team_mapping'),
    path('api/coachToTeam/teamsByCoach/<int:coach_id>/', teams_by_coach_id, name='teams_by_coach_id'),


    path('api/mapping/contestToJudge/create/', create_contest_judge_mapping, name='create_contest_judge_mapping'),
    path('api/mapping/contestToJudge/getContestByJudge/<int:judge_id>/', get_contest_id_by_judge_id, name='get_contest_id_by_judge_id'),
    path('api/mapping/contestToJudge/delete/<int:map_id>/', delete_contest_judge_mapping_by_id, name='delete_contest_judge_mapping'),

    path('api/mapping/contestToTeam/create/', create_contest_team_mapping, name='create_contest_team_mapping'),
    path('api/mapping/contestToTeam/getContestByTeam/<int:team_id>/', get_contest_id_by_team_id, name='get_contest_id_by_team_id'),
    path('api/mapping/contestToTeam/delete/<int:map_id>/', delete_contest_team_mapping_by_id, name='delete_contest_team_mapping'),

    path('api/mapping/contestToOrganizer/create/', create_contest_organizer_mapping, name='create_contest_organizer_mapping'),
    path('api/mapping/contestToOrganizer/getByOrganizer/<int:organizer_id>/', get_contests_by_organizer_id, name='get_contests_by_organizer_id'),
    path('api/mapping/contestToOrganizer/delete/<int:map_id>/', delete_contest_organizer_mapping_by_id, name='delete_contest_organizer_mapping'),

    path('api/mapping/judgeToContest/getAllJudges/<int:contest_id>/', get_all_judges_by_contest_id, name='get_all_judges_by_contest_id'),
    path('api/mapping/teamToContest/getTeamsByContest/<int:contest_id>/', get_teams_by_contest_id, name='get_teams_by_contest_id'),
    path('api/mapping/organizerToContest/getOrganizersByContest/<int:contest_id>/', get_organizers_by_contest_id, name='get_organizers_by_contest_id'),

    path('api/mapping/userToRole/create/', create_user_role_mapping, name='create_user_role_mapping'),
    path('api/mapping/userToRole/delete/<int:mapping_id>/', delete_user_role_mapping, name='delete_user_role_mapping'),
    path('api/mapping/userToRole/getUserByRole/<int:relatedid>/<int:roleType>/', get_user_by_role, name='get_user_by_role'),

    path('api/mapping/clusterToTeam/create/', create_cluster_team_mapping, name='create_cluster_team_mapping'),
    path('api/mapping/clusterToTeam/delete/<int:map_id>/', delete_cluster_team_mapping_by_id, name='delete_cluster_team_mapping'),
    path('api/mapping/clusterToTeam/getAllTeamsByCluster/<int:cluster_id>/', teams_by_cluster_id, name='teams_by_cluster'),
    path('api/mapping/clusterToTeam/getClusterByTeam/<int:team_id>/', cluster_by_team_id, name='cluster_by_team'),

    path('api/mapping/clusterToJudge/create/', create_cluster_judge_mapping, name='create_cluster_judge_mapping'),
    path('api/mapping/clusterToJudge/delete/<int:map_id>/', delete_cluster_judge_mapping_by_id, name='delete_cluster_judge_mapping'),
    path('api/mapping/clusterToJudge/getAllJudgesByCluster/<int:cluster_id>/', judges_by_cluster_id, name='judges_by_cluster'),
    path('api/mapping/clusterToJudge/getClusterByJudge/<int:judge_id>/', cluster_by_judge_id, name='cluster_by_judge'),

    path('api/mapping/clusterToContest/getAllClustersByContest/<int:contest_id>/', all_clusters_by_contest_id, name='all_clusters_by_contest_id'),

    path('api/mapping/scoreSheet/create/', create_score_sheet_mapping, name='create_score_sheet_mapping'),
    path('api/mapping/scoreSheet/getByTeamJudge/<int:sheetType>/<int:judge_id>/<int:team_id>/', score_sheet_by_judge_team, name='score_sheets_by_judge_team'),
    path('api/mapping/scoreSheet/delete/', delete_score_sheet_mapping_by_id, name='delete_score_sheet_mapping_by_id'),

    # Clusters
    path('api/cluster/get/<int:cluster_id>/', cluster_by_id, name='cluster_by_id'),
    path('api/cluster/getAll/', clusters_get_all, name='clusters_get_all'),
    path('api/cluster/create/', create_cluster, name='create_cluster'),
    path('api/cluster/edit/', edit_cluster, name='edit_cluster'),
    path('api/cluster/delete/<int:cluster_id>/', delete_cluster, name='delete_cluster'),

    # Contests
    path('api/contest/get/<int:contest_id>/', contest_by_id, name='contest_by_id'),
    path('api/contest/getAll/', contest_get_all, name='contest_get_all'),
    path('api/contest/create/', create_contest, name='create_contest'),
    path('api/contest/edit/', edit_contest, name='edit_contest'),
    path('api/contest/delete/<int:contest_id>/', delete_contest, name='delete_contest'),

    # ScoreSheets
    path('api/scoreSheet/get/<int:scores_id>/', scores_by_id, name='scores_by_id'),
    path('api/scoreSheet/create/', create_score_sheet, name='create_score_sheets'),
    path('api/scoreSheet/edit/', edit_score_sheet, name='edit_score_sheets'),
    path('api/scoreSheet/delete/<int:scores_id>/', delete_score_sheet, name='delete_score_sheets'),
    path('api/scoreSheet/edit/editField/', edit_score_sheet_field, name='edit_score_sheet_field'),
    path('api/scoreSheet/edit/updateScores/', update_scores, name='update_scores'),

    # Tabulation
    path('api/tabulation/tabulateScores/',tabulate_scores, name='tabulate_scores')
    
]