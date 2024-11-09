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
from ...models import JudgeClusters, Teams, MapClusterToTeam
from ...serializers import TeamSerializer, ClusterToTeamSerializer, JudgeClustersSerializer
from rest_framework.exceptions import ValidationError


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cluster_team_mapping(request):
    serializer = ClusterToTeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mapping": serializer.data}, status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def teams_by_cluster_id(request, cluster_id):
    mappings = MapClusterToTeam.objects.filter(clusterid=cluster_id)
    team_ids = mappings.values_list('teamid', flat=True)
    teams = Teams.objects.filter(id__in=team_ids)

    serializer = TeamSerializer(teams, many=True)

    return Response({"Teams": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cluster_by_team_id(request, team_id):
    try:
        mapping = MapClusterToTeam.objects.get(teamid=team_id)
        cluster_id = mapping.clusterid
        cluster = JudgeClusters.objects.get(id=cluster_id)
        serializer = JudgeClustersSerializer(instance=cluster)
        return Response({"Cluster": serializer.data}, status=status.HTTP_200_OK)
    except MapClusterToTeam.DoesNotExist:
        return Response({"error": "No cluster found for the given team"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cluster_team_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapClusterToTeam, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Cluster To Team Mapping deleted successfully."}, status=status.HTTP_200_OK)


def create_team_to_cluster_map(map_data):
  serializer = ClusterToTeamSerializer(data=map_data)
  if serializer.is_valid():
    serializer.save()
    return serializer.data
  else:
    return ValidationError(serializer.errors)

def rank_cluster_and_return_winner(clusterid):
  cluster_team_mappings = MapClusterToTeam.objects.filter(id==clusterid)
  clusterteams = Teams.objects.filter(id__in=cluster_team_mappings.values_list('teamid', flat=True))
  clusterteams.sort(key=lambda x: x.total_score, reverse=True)
  for x in range(len(clusterteams)):
    clusterteams[x].cluster_rank = x+1
  
  return clusterteams[x]


