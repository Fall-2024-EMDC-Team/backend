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

from ..models import Judge
from ..serializers import JudgeSerializer

@api_view(["GET"])
def judge_by_id(request, judge_id):  # Consistent parameter name
    judge = get_object_or_404(Judge, id=judge_id)  # Use user_id here
    serializer = JudgeSerializer(instance=judge)
    return Response({"Judge": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_judge(request):
    serializer = JudgeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # add user to DB
        return Response({"judge": serializer.data},status=status.HTTP_200_OK)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_judge(request):
    judge = get_object_or_404(Judge, id=request.data["id"])
    judge.first_name = request.data["first_name"]
    judge.last_name = request.data["last_name"]
    judge.presentation = request.data["presentation"]
    judge.mdo = request.data["mdo"]
    judge.journal = request.data["journal"]
    judge.penalties = request.data["penalties"]
    judge.save()

    serializer = JudgeSerializer(instance=judge)
    return Response({"judge": serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_judge(request, judge_id):
    judge = get_object_or_404(Judge, id=judge_id)
    judge.delete()
    return Response({"detail": "Judge deleted successfully."}, status=status.HTTP_200_OK)