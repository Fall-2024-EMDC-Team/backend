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
from ...models import JudgeClusters, Judge, MapJudgeToCluster
from ...serializers import JudgeClustersSerializer, JudgeSerializer, ClusterToJudgeSerializer


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cluster_judge_mapping(request):
    try:
        map_data = request.data
        result = map_cluster_to_judge(map_data)
        return Response(result, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def judges_by_cluster_id(request, cluster_id):
    mappings = MapJudgeToCluster.objects.filter(clusterid=cluster_id)
    judge_ids = mappings.values_list('judgeid', flat=True)
    judges = Judge.objects.filter(id__in=judge_ids)

    serializer = JudgeSerializer(judges, many=True)

    return Response({"Judges": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cluster_by_judge_id(request, judge_id):
    try:
        mapping = MapJudgeToCluster.objects.get(judgeid=judge_id)
        cluster_id = mapping.clusterid
        cluster = JudgeClusters.objects.get(id=cluster_id)
        serializer = JudgeClustersSerializer(instance=cluster)
        return Response({"Cluster": serializer.data}, status=status.HTTP_200_OK)
    except MapJudgeToCluster.DoesNotExist:
        return Response({"error": "No cluster found for the given judge"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cluster_judge_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapJudgeToCluster, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Cluster To Judge Mapping deleted successfully."}, status=status.HTTP_200_OK)


def delete_cluster_judge_mapping(map_id):
    # python can't overload functions >:(
    map_to_delete = get_object_or_404(MapJudgeToCluster, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Cluster To Judge Mapping deleted successfully."}, status=status.HTTP_200_OK)


def map_cluster_to_judge(map_data):
    serializer = ClusterToJudgeSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)
    
def judges_by_cluster(cluster_id):
    mappings = MapJudgeToCluster.objects.filter(clusterid=cluster_id)
    judge_ids = mappings.values_list('judgeid', flat=True)
    judges = Judge.objects.filter(id__in=judge_ids)

    serializer = JudgeSerializer(judges, many=True)

    return Response({"Judges": serializer.data}, status=status.HTTP_200_OK)