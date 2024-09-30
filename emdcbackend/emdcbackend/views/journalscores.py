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

from ..models import JournalScores
from ..serializers import JournalScoresSerializer

@api_view(["GET"])
def journal_scores_by_id(request, journal_scores_id):
    journal_scores = get_object_or_404(JournalScores, id=journal_scores_id)
    serializer = JournalScoresSerializer(instance=journal_scores)
    return Response({"JournalScores": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_journal_scores(request):
    serializer = JournalScoresSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"journal_scores": serializer.data})
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_journal_scores(request):
    journal_scores = get_object_or_404(JournalScores, id=request.data["id"])
    journal_scores.field1 = request.data["field1"]
    journal_scores.field2 = request.data["field2"]
    journal_scores.field3 = request.data["field3"]
    journal_scores.field4 = request.data["field4"]
    journal_scores.field5 = request.data["field5"]
    journal_scores.field6 = request.data["field6"]
    journal_scores.field7 = request.data["field7"]
    journal_scores.field8 = request.data["field8"]
    journal_scores.save()

    serializer = JournalScoresSerializer(instance=journal_scores)
    return Response({"journal_scores": serializer.data})

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_journal_scores(request, journal_scores_id):
    journal_scores = get_object_or_404(JournalScores, id=journal_scores_id)
    journal_scores.delete()
    return Response({"detail": "JournalScores deleted successfully."}, status=status.HTTP_200_OK)