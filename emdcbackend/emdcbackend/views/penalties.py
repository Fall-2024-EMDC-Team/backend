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

from ..models import Penalties
from ..serializers import PenaltiesSerializer

@api_view(["GET"])
def penalties_by_id(request, penalties_id):
    penalties = get_object_or_404(Penalties, id=penalties_id)
    serializer = PenaltiesSerializer(instance=penalties)
    return Response({"Penalties": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_penalties(request):
    serializer = PenaltiesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"create_penalties": serializer.data})
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_penalties(request):
    penalties = get_object_or_404(Penalties, id=request.data["id"])
    penalties.PresentationPenalties = request.data["PresentationPenalties"]
    penalties.MachinePenalties = request.data["MachinePenalties"]
    penalties.save()
    serializer = PenaltiesSerializer(instance=penalties)
    return Response({"edit_penalties": serializer.data})

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_penalties(request, penalties_id):
    penalties = get_object_or_404(Penalties, id=penalties_id)
    penalties.delete()
    return Response({"detail": "Penalties deleted successfully."}, status=status.HTTP_200_OK)
