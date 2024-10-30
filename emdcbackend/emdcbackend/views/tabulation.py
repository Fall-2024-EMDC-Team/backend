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

from ..models import Teams, Scoresheet, MapScoresheetToTeamJudge, MapContestToTeam, ScoresheetEnum
from ..serializers import TeamSerializer, ScoresheetSerializer

# reference for this file's functions will be in a markdown file titled *Scoring Tabultaion Outline* in the onedrive

@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tabulate_scores(request):
  contest_team_ids = MapContestToTeam.objects.filter(request.data["id"])
  contestteams = []
  for mapping in contest_team_ids:
    tempteam = Teams.objects.get(id=mapping.teamid)
    if tempteam:
      contesteams.append(tempteam)
    else:
      return Response({"Error: Team Not Found"},status=status.HTTP_404_NOT_FOUND)
  
  # at this point, we should have all of the teams for the contest, and we're going to go tabulate all of the total scores.

  for team in contestteams:
    # for each team, we're going to go get the team's scoresheets,
    score_sheet_ids = MapScoresheetToTeamJudge.objects.filter(teamid=team.id)
    scoresheets = []
    for mapping in score_sheet_ids:
      tempscoresheet = Scoresheet.objects.get(id=mapping.scoresheetid)
      if tempscoresheet:
        scoresheets.append(tempscoresheet)
      else:
        return Response({"Error: Score Sheet Data Not Found from Mapping!"},status=status.HTTP_404_NOT_FOUND)
    
    # tabulation time!
    totalscores = [0] * 12
    for scoresheet in scoresheets:
      if scoresheet.sheetType == ScoresheetEnum.PRESENTATION:
        totalscores[0] = totalscores[0] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
        totalscores[1] += 1
      elif scoresheet.sheetType == ScoresheetEnum.JOURNAL:
        totalscores[2] = totalscores[1] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
        totalscores[3] += 1
      elif scoresheet.sheetType == ScoresheetEnum.MACHINEDESIGN:
        totalscores[4] = totalscores[2] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
        totalscores[5] += 1
      elif scoresheet.sheetType == ScoresheetEnum.PENALTIES:
        # penalties are kinda tricky, so we're commenting this one out a bit. 
        # first thing we check for is the journal penalties and machine spec penalties. to my knowledge, these are not averaged and are calculated once.
        totalscores[6] = scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5
        totalscores[7] += 1
        # we then check for if there is penalties for run 1, and add the counter for run1 with that
        totalscores[8] = totalscores[8] + scoresheet.field6+ scoresheet.field7+ scoresheet.field8 + scoresheet.field9 + scoresheet.field10 + scoresheet.field11 + scoresheet.field12 + scoresheet.field13
        totalscores[9] += 1
        # we then grab the penalties for run2
        totalscores[10] = totalscores[10] + scoresheet.field14+ scoresheet.field15+ scoresheet.field16 + scoresheet.field17 + scoresheet.field18 + scoresheet.field19 + scoresheet.field20 + scoresheet.field21
        totalscores[11] += 1
    # scores are compiled, time to get final scores and save it all up
    team.presentation_score = totalscores[0] / totalscores[1]
    team.journal_score = totalscores[2] / totalscores[3]
    team.machinedesign_score = totalscores[4] / totalscores[5]
    team.penalties_score = totalscores[6] / totalscores[7] + totalscores[8]/totalscores[9] +  totalscores[10]/totalscores[11]
    team.total_score = (team.presentation_score + team.journal_score + team.machinedesign_score) - team.penalties
    team.save()

  return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_teams_by_total_score(request):
  contest_team_ids = MapContestToTeam.objects.filter(request.data["id"])
  contestteams = []
  for mapping in contest_team_ids:
    tempteam = Teams.objects.get(id=mapping.teamid)
    if tempteam:
      contesteams.append(tempteam)
    else:
      return Response({"Error: Team Not Found"},status=status.HTTP_404_NOT_FOUND)

  # next goal: sort the array of teams by their total score!
  contestteams.sort(key=lambda x: x.total_score, reverse=True)
  serializer = TeamSerializer(instance=contestteams, many=True)
  return Response({"Teams":serializer.data},status=status.HTTP_200_OK)


'''
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_scoresheet_comments_by_team_id(request):
  scoresheeids = MapScoresheetToTeamJudge.objects.filter(teamid=request.data["teamid"])
  scoresheets = Scoresheet.objects.filter(id__in=scoresheeids)
''' 
  
  
    
  
      


    

    

