from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ...models import MapCoachToTeam, Coach, Teams
from ...serializers import CoachToTeamSerializer

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_coach_team_mapping(request):
    serializer = CoachToTeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mapping": serializer.data},status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def teams_by_coach_id(request, coach_id):
    team_mappings = MapCoachToTeam.objects.filter(uuid=coach_id)
    team_ids = team_mappings.values_list('teamid', flat=True)
    teams = Teams.objects.filter(id__in=team_ids)

    # serializer = TeamsSerializer(teams, many=True)

    return Response({"Teams": list(teams.values())}, status=status.HTTP_200_OK)
