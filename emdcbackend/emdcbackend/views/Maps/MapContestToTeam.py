from django.core.exceptions import FieldError
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
    try:
      mappings = MapContestToTeam.objects.filter(contestid=contest_id)
      team_ids = mappings.values_list('teamid',flat=True)
      teams = Teams.objects.filter(id__in=team_ids).order_by('team_rank')
      serializer = TeamSerializer(teams, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_contests_by_team_ids(request):
    try:
        # Extract team IDs from the request data
        team_ids = [team["id"] for team in request.data if "id" in team]

        # Fetch mappings for the specified team IDs
        mappings = MapContestToTeam.objects.filter(teamid__in=team_ids)

        # Gather unique contest IDs from the mappings
        contest_ids = set(mapping.contestid for mapping in mappings)

        # Fetch the Contest objects based on these contest IDs
        contests = Contest.objects.filter(id__in=contest_ids)
        contest_data = {contest.id: ContestSerializer(contest).data for contest in contests}

        # Map each team ID to its contest data based on the mappings
        result = {
            mapping.teamid: contest_data.get(mapping.contestid)
            for mapping in mappings
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # General exception handling
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contest_team_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapContestToTeam, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Contest To Team Mapping deleted successfully."}, status=status.HTTP_200_OK)


def create_team_to_contest_map(map_data):
  serializer = MapContestToTeamSerializer(data=map_data)
  if serializer.is_valid():
    serializer.save()
    return serializer.data
  else:
    raise ValidationError(serializer.errors)
