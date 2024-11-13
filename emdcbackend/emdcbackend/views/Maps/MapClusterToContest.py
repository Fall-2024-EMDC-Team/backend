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
from ...models import JudgeClusters, Contest, MapContestToCluster
from ...serializers import JudgeClustersSerializer, ContestSerializer, ClusterToContestSerializer


# make non http request to create mapping
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cluster_contest_mapping(request):
    try:
        map_data = request.data
        result = map_cluster_to_contest(map_data)
        return Response(result, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def contests_by_cluster_id(request, cluster_id):
    mappings = MapContestToCluster.objects.filter(clusterid=cluster_id)
    contest_ids = mappings.values_list('contestid', flat=True)
    contests = Contest.objects.filter(id__in=contest_ids)

    serializer = ContestSerializer(contests, many=True)

    return Response({"Contests": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cluster_by_contest_id(request, contest_id):
    try:
        mapping = MapContestToCluster.objects.get(judgeid=contest_id)
        cluster_id = mapping.clusterid
        cluster = JudgeClusters.objects.get(id=cluster_id)
        serializer = JudgeClustersSerializer(instance=cluster)
        return Response({"Cluster": serializer.data}, status=status.HTTP_200_OK)
    
    except MapContestToCluster.DoesNotExist:
        return Response({"error": "No cluster found for the given contest"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cluster_contest_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapContestToCluster, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Cluster To Contest Mapping deleted successfully."}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_clusters_by_contest_id(request, contest_id):
    try:
        mappings = MapContestToCluster.objects.filter(contestid=contest_id)
        cluster_ids = mappings.values_list('clusterid', flat=True)
        clusters = JudgeClusters.objects.filter(id__in=cluster_ids)
        serializer = JudgeClustersSerializer(clusters, many=True)
        return Response({"Clusters": serializer.data}, status=status.HTTP_200_OK)
    
    except MapContestToCluster.DoesNotExist:
        return Response({"error": "No clusters found for the given contest"}, status=status.HTTP_404_NOT_FOUND)

        
def map_cluster_to_contest(map_data):
    serializer = ClusterToContestSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)

def get_all_teams_cluster(contest_id):
    try:
        # Get all "All Teams" clusters IDs
        all_teams_clusters = JudgeClusters.objects.filter(cluster_name="All Teams")
        cluster_ids = all_teams_clusters.values_list('id', flat=True)

        # Get the mapping for the specified contest and any "All Teams" cluster
        cluster_mapping = MapContestToCluster.objects.filter(
            clusterid__in=cluster_ids, contestid=contest_id
        ).first()  # Use `first()` since there's only one expected result

        if not cluster_mapping:
            return {"error": "No 'All Teams' cluster mapping found for this contest."}, None

        # Retrieve the specific JudgeClusters object based on the cluster ID in the mapping
        cluster = JudgeClusters.objects.get(id=cluster_mapping.clusterid)
        serializer = JudgeClustersSerializer(cluster).data.get("id")

        return serializer  # Return the cluster object

    except JudgeClusters.DoesNotExist:
        return {"error": "'All Teams' cluster not found."}, None
    except Exception as e:
        print(f"Error retrieving 'All Teams' cluster: {str(e)}")
        return {"error": str(e)}, None

