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

from ..models import Teams, Scoresheet, MapScoresheetToTeamJudge, MapContestToTeam, ScoresheetEnum, MapClusterToTeam, JudgeClusters, MapContestToCluster

# reference for this file's functions will be in a markdown file titled *Scoring Tabultaion Outline* in the onedrive

@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tabulate_scores(request):
  contest_team_ids = MapContestToTeam.objects.filter(contestid=request.data["contestid"])

  contestteams = []
  for mapping in contest_team_ids:
    tempteam = Teams.objects.get(id=mapping.teamid)
    if tempteam:
      contestteams.append(tempteam)
    else:
      return Response({"Error: Team Not Found"},status=status.HTTP_404_NOT_FOUND)
  
  contest_cluster_ids = MapContestToCluster.objects.filter(contestid=request.data["contestid"])
  clusters = []
  for mapping in contest_cluster_ids:
    tempcluster = JudgeClusters.objects.get(id=mapping.clusterid)
    if tempcluster:
      clusters.append(tempcluster)
    else:
      return Response({"Error: Cluster Not Found"},status=status.HTTP_404_NOT_FOUND)
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
    # initialize a temp array to hold scores
    totalscores = [0] * 11
    for scoresheet in scoresheets:
      if scoresheet.isSubmitted:
          # We're going to keep track for each sheet type how many times we've seen the type, since for each of the sheets we're taking the average of the scores.
        if scoresheet.sheetType == ScoresheetEnum.PRESENTATION:
          totalscores[0] = totalscores[0] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
          totalscores[1] += 1

        elif scoresheet.sheetType == ScoresheetEnum.JOURNAL:
          totalscores[2] = totalscores[2] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
          totalscores[3] += 1

        elif scoresheet.sheetType == ScoresheetEnum.MACHINEDESIGN:
          totalscores[4] = totalscores[4] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3+ scoresheet.field4+ scoresheet.field5+ scoresheet.field6+ scoresheet.field7+ scoresheet.field8
          totalscores[5] += 1

        elif scoresheet.sheetType == ScoresheetEnum.RUNPENALTIES:
          # we then check for if there is penalties for run 1, and increment the counter since run penalties are taken as an average
          totalscores[7] = totalscores[8] + scoresheet.field1+ scoresheet.field2+ scoresheet.field3 + scoresheet.field4 + scoresheet.field5 + scoresheet.field6 + scoresheet.field7 + scoresheet.field8
          totalscores[8] += 1
          # we then grab the penalties for run2 and do same style of calculation that we did for run1
          totalscores[9] = totalscores[10] + scoresheet.field10+ scoresheet.field11+ scoresheet.field12 + scoresheet.field13 + scoresheet.field14 + scoresheet.field15 + scoresheet.field16 + scoresheet.field17
          totalscores[10] += 1

        elif scoresheet.sheetType == ScoresheetEnum.OTHERPENALTIES:
          totalscores[6] = + scoresheet.field1+ scoresheet.field2+ scoresheet.field3 + scoresheet.field4 + scoresheet.field5 + scoresheet.field6 + scoresheet.field7
    # scores are compiled but not averaged yet, we're going to average the scores and then save that score as the total score. 

    # problem statement: 
    team.presentation_score = totalscores[0] / totalscores[1]
    team.journal_score = totalscores[2] / totalscores[3]
    team.machinedesign_score = totalscores[4] / totalscores[5]

    team.penalties_score = totalscores[6] + totalscores[7]/totalscores[8] +  totalscores[9]/totalscores[10]
    team.total_score = (team.presentation_score + team.journal_score + team.machinedesign_score) - team.penalties_score
    team.save()

  # this is where we set the ranks for the teams in terms of clusters and contest.
  for cluster in clusters:
    set_cluster_rank({"clusterid":cluster.id})
  set_team_rank({"contestid":request.data["contestid"]})

  return Response(status=status.HTTP_200_OK)

# this function iterates through each team in the contest and sets the rank of the team based on the total score.
def set_team_rank(data):
  contest_team_ids = MapContestToTeam.objects.filter(contestid = data["contestid"])
  contestteams = []
  for mapping in contest_team_ids:
    tempteam = Teams.objects.get(id=mapping.teamid)
    if tempteam:
      if not tempteam.organizer_disqualified:
        contestteams.append(tempteam)
    else:
      raise ValidationError('Team Cannot Be Found.')
  # next goal: sort the array of teams by their total score!
  contestteams.sort(key=lambda x: x.total_score, reverse=True)
  for x in range(len(contestteams)):
    contestteams[x].team_rank = x+1
    contestteams[x].save()
  return

# function to set the rank of the teams in a cluster
def set_cluster_rank(data):
    cluster_team_ids = MapClusterToTeam.objects.filter(clusterid=data["clusterid"])
    clusterteams = []
    for mapping in cluster_team_ids:
      tempteam = Teams.objects.get(id=mapping.teamid)
      if tempteam:
        if not tempteam.organizer_disqualified:
          clusterteams.append(tempteam)
      else:
        raise ValidationError('Team Cannot Be Found.')
    clusterteams.sort(key=lambda x: x.total_score, reverse=True)
    for x in range(len(clusterteams)):
        clusterteams[x].cluster_rank = x+1
        clusterteams[x].save()
    return 

# function to get all scoresheets that a team has submitted
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_scoresheet_comments_by_team_id(request):
  scoresheeids = MapScoresheetToTeamJudge.objects.filter(teamid=request.data["teamid"])
  scoresheets = Scoresheet.objects.filter(id__in=scoresheeids)
  comments = []
  for sheet in scoresheets:
    if sheet.field9 != "":
      comments.append(sheet.field9),
  return Response({"Comments": comments}, status=status.HTTP_200_OK)

    

    

