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
from ..models import JudgeClusters
from ..serializers import JudgeClustersSerializer

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cluster_by_id(request, cluster_id):
  cluster = get_object_or_404(JudgeClusters, id = cluster_id)
  serializer = JudgeClustersSerializer(instance=cluster)
  return Response({"Cluster": serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def clusters_get_all(request):
  clusters = JudgeClusters.objects.all()
  serializer = JudgeClustersSerializer(clusters, many=True)
  return Response({"Clusters":serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cluster(request):
    if JudgeClusters.objects.filter(cluster_name=request.data["cluster_name"]).exists():
        return Response(
            {"detail": "A cluster with this name already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = JudgeClustersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"cluster": serializer.data},status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_cluster(request):
    cluster = get_object_or_404(JudgeClusters, id=request.data["id"])

    if (JudgeClusters.objects.filter(cluster_name=request.data["cluster_name"]).exists() and
            request.data["cluster_name"] != cluster.cluster_name):
        return Response(
            {"detail": "A cluster with this name already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    cluster.cluster_name = request.data["cluster_name"]
    cluster.save()

    serializer = JudgeClustersSerializer(instance=cluster)
    return Response({"cluster": serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cluster(request, cluster_id):
    cluster = get_object_or_404(JudgeClusters, id=cluster_id)
    cluster.delete()
    return Response({"detail": "Cluster deleted successfully."}, status=status.HTTP_200_OK)