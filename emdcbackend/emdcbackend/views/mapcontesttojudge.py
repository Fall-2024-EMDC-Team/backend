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

from ..models import MapContestToJudge
from ..serializers import MapContestToJudgeSerializer

@api_view(['GET'])
def get_all_judges_by_contest_id(request,contest_id):
    payload = MapContestToJudge.objects.filter(request.data["id"])
    serializer = MapContestToJudgeSerializer(instance=payload)
    return Response({"Judge IDs":serializer.data},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_contest_id_by_judge_id(request):
    payload = MapContestToJudge.objects.get(judgeid=request.data["id"])
      #if payload =
    serializer = MapContestToJudgeSerializer(instance=payload)
    return Response({"Contest ID":serializer.data},status=status.HTTP_200_OK)