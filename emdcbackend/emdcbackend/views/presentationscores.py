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

from ..models import PresentationScores
from ..serializers import PresentationScoresSerializer

@api_view(["GET"])
def presentation_scores_by_id(request, presentation_scores_id):
    presentation_scores = get_object_or_404(PresentationScores, id=presentation_scores_id)
    serializer = PresentationScoresSerializer(instance=presentation_scores)
    return Response({"PresentationScores": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_presentation_scores(request):
    serializer = PresentationScoresSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"presentation_scores": serializer.data})
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_presentation_scores(request):
    presentation_scores = get_object_or_404(PresentationScores, id=request.data["id"])
    presentation_scores.field1 = request.data["field1"]
    presentation_scores.field2 = request.data["field2"]
    presentation_scores.field3 = request.data["field3"]
    presentation_scores.field4 = request.data["field4"]
    presentation_scores.field5 = request.data["field5"]
    presentation_scores.field6 = request.data["field6"]
    presentation_scores.field7 = request.data["field7"]
    presentation_scores.field8 = request.data["field8"]
    presentation_scores.save()

    serializer = PresentationScoresSerializer(instance=presentation_scores)
    return Response({"presentation_scores": serializer.data})

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_presentation_scores(request, presentation_scores_id):
    presentation_scores = get_object_or_404(PresentationScores, id=presentation_scores_id)
    presentation_scores.delete()
    return Response({"detail": "PresentationScores deleted successfully."}, status=status.HTTP_200_OK)