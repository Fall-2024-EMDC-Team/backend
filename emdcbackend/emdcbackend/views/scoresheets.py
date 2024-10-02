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

from ..models import Scoresheet
from ..serializers import ScoresheetSerializer

@api_view(["GET"])
def scores_by_id(request, scores_id):
    scores = get_object_or_404(Scoresheet, id=scores_id)
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"Scores": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_score_sheets(request):
    serializer = ScoresheetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"create_score_sheets": serializer.data})
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_score_sheets(request):
    scores = get_object_or_404(Scoresheet, id=request.data["id"])
    scores.sheetType = request.data["sheetType"]
    scores.field1 = request.data["field1"]
    scores.field2 = request.data["field2"]
    scores.field3 = request.data["field3"]
    scores.field4 = request.data["field4"]
    scores.field5 = request.data["field5"]
    scores.field6 = request.data["field6"]
    scores.field7 = request.data["field7"]
    scores.field8 = request.data["field8"]
    scores.save()
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"edit_score_sheets": serializer.data})

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_score_sheets(request, scores_id):
    scores = get_object_or_404(Scoresheet, id=scores_id)
    scores.delete()
    return Response({"detail": "Score Sheet deleted successfully."}, status=status.HTTP_200_OK)