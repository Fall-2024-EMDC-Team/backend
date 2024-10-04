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
from ...models import MapContestToTeam, Contest, Teams
from ...serializers import MapContestToTeamSerializer, ContestSerializer, TeamSerializer

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contest_team_mapping(request):
  serializer = MapContestToTeamSerializer(data=request.data)
  if serializer.is_valid():
      serializer.save()
      return Response({"mapping": serializer.data},status=status.HTTP_200_OK)
  return Response(
      serializer.errors, status=status.HTTP_400_BAD_REQUEST
  )

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_teams_by_contest_id(request,contest_id):
  mappings = MapContestToTeam.objects.filter(contestid=contest_id)
  team_ids = mappings.values_list('teamid',flat=True)
  teams = Teams.objects.filter(id__in=team_ids)

  # implement and change this into the serializer once the teams stuff is done

  return Response("This Call is Unfinished",status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_contest_id_by_team_id(request,team_id):
  try:
    map = MapContestToTeam.objects.get(teamid=team_id)
    contest_id=map.contestid
    contest=Contest.objects.get(id=contest_id)
    serializer = ContestSerializer(instance=contest)
    return Response({"Contest":serializer.data},status=status.HTTP_200_OK)
  except MapContestToTeam.DoesNotExist:
    return Response({"error: No Contest Found for given Team"},status=status.http_404)
  
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contest_team_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapContestToTeam, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Contest To Team Mapping deleted successfully."}, status=status.HTTP_200_OK)