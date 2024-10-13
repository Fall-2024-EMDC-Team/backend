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
from .Maps.MapClusterToContest import  create_cluster_contest_mapping

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
            if JudgeClusters.objects.filter(cluster_name=request.data["cluster_name"]).exists():
                return Response(
                    {"detail": "A cluster with this name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = JudgeClustersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # map team to cluster
                responses = [
                    create_cluster_contest_mapping({
                    "contestid": request.data["contestid"],
                    "clusterid": request.data["clusterid"]
                    })
                ]
                # Check for any errors in mapping responses
                for response in responses:
                    if isinstance(response, Response):
                        return response

                return Response({"cluster": serializer.data},status=status.HTTP_200_OK)
            
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    except ValidationError as e:  # Catching ValidationErrors specifically
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(["POST"])  # map judge and team to cluster
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def create_cluster(request):
   
#    responses = [
#          create_cluster_team_mapping({
#             "teamid": request.data["teamid"],
#             "clusterid": request.data["clusterid"]
#          })
#    ]
#     # Check for any errors in mapping responses
#     for response in responses:
#         if isinstance(response, Response):
#             return response

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