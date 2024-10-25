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

from models import Teams, Scoresheet, MapScoresheetToTeamJudge, MapContestToTeam, ScoresheetEnum
from serializer import TeamSerializer

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
  
  # at this point, we should have a bunch of teams within this contestteams thing, and we're going to go cascading :D

  for team in contestteams:
    # for each team, we're going to go get the team's scoresheets, and then begin tabulating
    score_sheet_ids = MapScoresheetToTeamJudge.objects.filter(teamid=team.id)
    scoresheets = []
    for mapping in score_sheet_ids:
      tempscoresheet = Scoresheet.objects.get(id=mapping.scoresheetid)
      if tempscoresheet:
        scoresheets.append(tempscoresheet)
      else:
        return Response({"Error: Score Sheet Data Not Found from Mapping!"},status=status.HTTP_404_NOT_FOUND)
    
    totalscores = []
    for scoresheet in scoresheets:
      if scoresheet.sheetType == ScoresheetEnum.PRESENTATION:
        totalscores[0] = totalscores[0] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
        totalscores[4] += 1
      elif scoresheet.sheetType == ScoresheetEnum.JOURNAL:
        totalscores[1] = totalscores[1] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
        totalscores[5] += 1
      elif scoresheet.sheetType == ScoresheetEnum.MACHINEDESIGN:
        totalscores[2] = totalscores[2] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
        totalscores[6] += 1
      elif scoresheet.sheetType == ScoresheetEnum.PENALTIES:
        

    

    

