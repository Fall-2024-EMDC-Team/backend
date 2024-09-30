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

from ..models import MachineDesignScores
from ..serializers import MachineDesignScoresSerializer

@api_view(["GET"])
def machine_design_scores_by_id(request, machine_design_scores_id):
    machine_design_scores = get_object_or_404(MachineDesignScores, id=machine_design_scores_id)
    serializer = MachineDesignScoresSerializer(instance=machine_design_scores)
    return Response({"MachineDesignScores": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_machine_design_scores(request):
    serializer = MachineDesignScoresSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"machine_design_scores": serializer.data})
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_machine_design_scores(request):
    machine_design_scores = get_object_or_404(MachineDesignScores, id=request.data["id"])
    machine_design_scores.field1 = request.data["field1"]
    machine_design_scores.field2 = request.data["field2"]
    machine_design_scores.field3 = request.data["field3"]
    machine_design_scores.field4 = request.data["field4"]
    machine_design_scores.field5 = request.data["field5"]
    machine_design_scores.field6 = request.data["field6"]
    machine_design_scores.field7 = request.data["field7"]
    machine_design_scores.field8 = request.data["field8"]
    machine_design_scores.save()

    serializer = MachineDesignScoresSerializer(instance=machine_design_scores)
    return Response({"machine_design_scores": serializer.data})

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_machine_design_scores(request, machine_design_scores_id):
    machine_design_scores = get_object_or_404(MachineDesignScores, id=machine_design_scores_id)
    machine_design_scores.delete()
    return Response({"detail": "MachineDesignScores deleted successfully."}, status=status.HTTP_200_OK)
