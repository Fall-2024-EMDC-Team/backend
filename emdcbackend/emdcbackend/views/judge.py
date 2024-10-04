from django.db import transaction
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

from .Maps.MapUserToRole import create_user_role_mapping, create_user_role_map
from ..auth.views import create_user
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
    try:
        with transaction.atomic():
            # Create user
            user_data = {
                "username":request.data["username"],
                "password":request.data["password"]
            }
            user_response = create_user(user_data)
            if isinstance(user_response, Response):
                return user_response

            # Create judge
            judge_data = {
                "first_name": request.data["first_name"],
                "last_name": request.data["last_name"],
                "contestid": request.data["contestid"],
                "presentation": request.data["presentation"],
                "mdo": request.data["mdo"],
                "journal": request.data["journal"],
                "penalties": request.data["penalties"],
            }
            judge_response = create_judge_instance(judge_data)
            if isinstance(judge_response, Response):
                return judge_response


            #map judge to user
            judge_to_user_data = {
                "uuid": user_response.get("user").get("id"),
                "role": 3,
                "relatedid": judge_response.get("id")
            }
            judge_to_user_response = create_user_role_map(judge_to_user_data)
            if isinstance(judge_to_user_response, Response):
                return judge_to_user_data

            return Response({"user": user_response, "judge": judge_response, "map": judge_to_user_response}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

def create_judge_instance(judge_data):
    serializer = JudgeSerializer(data=judge_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)