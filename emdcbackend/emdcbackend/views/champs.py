from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .Maps.MapClusterToTeam import rank_cluster_and_return_winner
from .team import make_team
from .contest import create_contest_instance
from .clusters import make_cluster
from .Maps.MapCoachToTeam import create_coach_to_team_map
from .Maps.MapContestToTeam import create_team_to_contest_map
from .Maps.MapClusterToTeam import create_team_to_cluster_map
from ..models import Teams, Scoresheet, Contest, MapScoresheetToTeamJudge, MapContestToTeam, ScoresheetEnum, MapContestToCluster, JudgeClusters, MapCoachToTeam, Coach, Judge, MapContestToJudge
from ..serializers import TeamSerializer, ScoresheetSerializer, ContestSerializer, MapScoresheetToTeamJudgeSerializer, MapContestToTeamSerializer

# this file is for all endpoints and functions that pertain to the implementation of Championship or Prelim/Finals type contests.

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_finals(request):
    #try:
        current_contest = get_object_or_404(Contest, id=request.data["id"])
        if current_contest.is_prelim != True:
          return Response({"Error: Current Contest is not eligible for a Prelim/Finals Split"},status=status.HTTP_403_FORBIDDEN)
        
        # make the contest!
        all_teams_cluster = make_cluster({"cluster_name": "All Teams"})
        contestresponse = create_contest_instance({"name": request.data["name"] + "Finals", "date": current_contest.date, "is_open":False,"is_tabulated":False, "is_prelim":False})
        responses = [
          map_cluster_to_contest({
              "contestid": contestresponse.get("id"),
              "clusterid": all_teams_cluster.get("id")
          }), 
        ]

        # now that we verify the contest, we grab the winner from each cluster and bring them into the list of teams to be brought over to the next contest.
        finalsteams = []
        
        cluster_mappings = MapContestToCluster.objects.filter(contestid==request.data["id"])
        clusters = JudgeClusters.objects.filter(id__in=cluster_mappings.values_list('clusterid', flat=True))
        for cluster in clusters:
          # each cluster winner gets added to the teams moving onto the finals 
          if cluster.cluster_name != "All Teams":
            finalsteams.append(rank_cluster_and_return_winner(cluster.id))
        teammappings = MapContestToTeam.objects.filter(contestid==request.data["id"])
        teams = Teams.objects.filter(id__in=teammappings.values_list('teamid',flat=True))
        contestteams.sort(key=lambda x: x.team_rank, reverse=True)
        # get the remaining number of teams desired added to finals based on team score.
        while len(finalsteams) < request.data["finalssize"]:
          for team in contestteams:
            if team not in finalsteams:
              finalsteams.append(team)
        TeamResponses = []
        # now we have all of the teams, we can move all the teams over to the new contest.
        for team in finalsteams:
          team_coach = get_object_or_404(Coach, id=MapCoachToTeam.objects.filter(id == team.id))

          TeamResponse = make_team({
            "team_name":team.name,
            "journal_score":team.journal_score,
            "presentation_score":0,
            "machinedesign_score":0,
            "penalties_score":0,
            "total_score":team.journal_score
            })
          
          ContestTeamMapping = create_team_to_contest_map({
            "contestid":contestresponse.get("id"),
            "teamid": TeamResponse.get("id")
          })

          CoachTeamMapping = create_coach_to_team_map({
            "teamid": TeamResponse.get("id"),
            "coachid": team_coach.id
          })

        # now 
      

          
          
          


          

