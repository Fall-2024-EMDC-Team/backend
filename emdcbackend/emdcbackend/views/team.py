from ..models import Teams, Scoresheet, JudgeClusters, Judge
from .Maps import MapScoreSheet
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeamSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction

# get team
@api_view(["GET"])
def team_by_id(request, team_id):
    team = get_object_or_404(Teams, id=team_id)
    serializer = TeamSerializer(instance=team)
    return Response({"Team": serializer.data}, status=status.HTTP_200_OK)

# create team
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_team(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # add team to DB
        return Response({"Team": serializer.data}, status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

# edit team
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_team(request):
    try:
        team = get_object_or_404(Teams, id=request.data["id"])
        old_team_name = team.team_name
        old_cluster = team.judge_cluster

        new_team_name = request.data["team_name"]
        new_journal_score = request.data["journal_score"]
        new_presentation_score = request.data["presentation_score"]
        new_machinedesign_score = request.data["machinedesign_score"]
        new_score_penalties = request.data["score_penalties"]
        new_cluster = request.data["judge_cluster"]
        
        with transaction.atomic():

            if old_team_name != new_team_name:
                team.team_name = new_team_name

            if old_cluster != new_cluster: 
                Scoresheet.objects.filter(team=team).delete()
                MapScoreSheet.objects.filter(team=team).delete()

                judges = JudgeClusters.objects.get(id=new_cluster).judges.all()
                for judge in judges:
                    score_sheet = Scoresheet.objects.create(judge=judge, team=team)
                    MapScoreSheet.objects.create(score_sheet=score_sheet, judge=judge, team=team)
                
            if team.journal_score != new_journal_score:
                team.journal_score = new_journal_score
            if team.presentation_score != new_presentation_score:
                team.presentation_score = new_presentation_score
            if team.machinedesign_score != new_machinedesign_score:
                team.machinedesign_score = new_machinedesign_score
            if team.score_penalties != new_score_penalties:
                team.score_penalties = new_score_penalties

            team.save()

        serializer = TeamSerializer(instance=team)

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"Team": serializer.data}, status=status.HTTP_200_OK)

# delete team
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_team_by_id(request, team_id):
    team_to_delete = get_object_or_404(Teams, id=team_id)
    team_to_delete.delete()
    return Response({"detail": "Team deleted successfully."}, status=status.HTTP_200_OK)
