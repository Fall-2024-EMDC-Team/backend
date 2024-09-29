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
from .views.Maps.MapCoachToTeam import create_coach_team_mapping, coach_by_team_id
from .views.Maps.MapContestToJudge import create_contest_judge_mapping,get_all_judges_by_contest_id,get_contest_id_by_judge_id

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
    path('contestByID/<int:contest_id>/', contest_by_id),
    path('contestGetAll/',contest_get_all),
    path('createContest/',create_contest),
    path('editContest/',edit_contest),
    path('deleteContest/<int:contest_id>/',delete_contest),
    path('mapContestToJudge/',create_contest_judge_mapping),
    path('getJudgesByContest/<int:contest_id>/',get_all_judges_by_contest_id),
    path('getContestByJudge/<int:judge_id>/',get_contest_id_by_judge_id),

]
