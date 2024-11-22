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
        # Get all mappings for the team
        mappings = MapClusterToTeam.objects.filter(teamid=team_id)

        # If no mappings are found, return an error
        if not mappings.exists():
            return Response({"error": "No clusters found for the given team"}, status=status.HTTP_404_NOT_FOUND)

        # Collect all cluster IDs from the mappings
        cluster_ids = [mapping.clusterid for mapping in mappings]

        # Get all clusters corresponding to the cluster IDs
        clusters = JudgeClusters.objects.filter(id__in=cluster_ids)

        # Serialize the clusters
        serializer = JudgeClustersSerializer(clusters, many=True)

        return Response({"Clusters": serializer.data}, status=status.HTTP_200_OK)

    except JudgeClusters.DoesNotExist:
        return Response({"error": "One or more clusters not found for the given IDs"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cluster_team_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapClusterToTeam, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Cluster To Team Mapping deleted successfully."}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_teams_by_cluster_rank(request):
    mappings = MapClusterToTeam.objects.filter(clusterid=request.data["clusterid"])
    teams = Teams.objects.filter(
        id__in=mappings.values_list('teamid', flat=True),
        cluster_rank__isnull=False
    ).order_by('cluster_rank')
    serializer = TeamSerializer(teams, many=True)
    return Response({"Teams": serializer.data}, status=status.HTTP_200_OK)
  

def create_team_to_cluster_map(map_data):
  serializer = ClusterToTeamSerializer(data=map_data)
  if serializer.is_valid():
    serializer.save()
    return serializer.data
  else:
    return ValidationError(serializer.errors)

