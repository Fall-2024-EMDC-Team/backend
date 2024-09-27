from models import Teams
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
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

# create team
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_team(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # add user to DB
        return Response({"team": serializer.data})
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

# edit team
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_user(request):
    team = get_object_or_404(Teams, id=request.data["teamid"])
    team.team_name = request.data=["team_name"]
    team.school_name = request.data=["school_name"]
    team.journal_score = request.data=["journal_score"]
    team.presentation_score = request.data=["team_name"]
    team.machinedesign_score = request.data=["machinedesign_score"]
    team.score_penalties = request.data=["score_penalties"]
    team.judge_cluster = request.data=["team_name"]
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
