from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from ..models import JudgeClusters
from ..serializers import JudgeClustersSerializer
from .Maps.MapClusterToContest import  map_cluster_to_contest
from ..models import Teams, MapClusterToTeam
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
  try:
    with transaction.atomic():
      cluster_response = make_cluster(request.data)
      responses = [
        map_cluster_to_contest({
          "contestid": request.data["contestid"],
          "clusterid": cluster_response.get("id")
        })
      ]
      
      # Check for any errors in mapping responses
      for response in responses:
        if isinstance(response, Response):
          return response

      return Response({
        "cluster": cluster_response,
        "cluster to contest map:": responses[0]
      }, status=status.HTTP_201_CREATED)

  except ValidationError as e:  # Catching ValidationErrors specifically
    return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  
  except Exception as e:
    return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_cluster(request):
    cluster = get_object_or_404(JudgeClusters, id=request.data["id"])
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


def make_judge_cluster_instance(data):
  serializer = JudgeClustersSerializer(data=data)
  if serializer.is_valid():
      serializer.save()
      return serializer.data
  raise ValidationError(serializer.errors)


def make_cluster(data):
  cluster_data = {"cluster_name":data["cluster_name"]}
  cluster_response = make_judge_cluster_instance(cluster_data)
  if not cluster_response.get('id'):
        raise ValidationError('Cluster creation failed.')
  return cluster_response

