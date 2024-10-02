from ..models import Teams
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeamSerializer
from django.shortcuts import get_object_or_404

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
    team = get_object_or_404(Teams, id=request.data["id"])
    team.team_name = request.data["team_name"]
    team.journal_score = request.data["journal_score"]
    team.presentation_score = request.data["presentation_score"]
    team.machinedesign_score = request.data["machinedesign_score"]
    team.score_penalties = request.data["score_penalties"]
    team.judge_cluster = request.data["judge_cluster"]
    team.save()

    serializer = TeamSerializer(instance=team)
    return Response({"team": serializer.data})

# delete team
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_team_by_id(request, team_id):
    team_to_delete = get_object_or_404(Teams, id=team_id)
    team_to_delete.delete()
    return Response({"detail": "Team deleted successfully."}, status=status.HTTP_200_OK)
