from django.db import transaction
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .Maps.MapUserToRole import create_user_role_map
from .Maps.MapContestToJudge import create_contest_to_judge_map
from .Maps.MapClusterToJudge import map_cluster_to_judge
from .scoresheets import create_sheets_for_teams_in_cluster
from ..auth.views import create_user
from ..models import Judge, Scoresheet, MapScoresheetToTeamJudge
from ..serializers import JudgeSerializer, MapScoreSheetToTeamJudgeSerializer


@api_view(["GET"])
def judge_by_id(request, judge_id):  # Consistent parameter name
    judge = get_object_or_404(Judge, id=judge_id)  # Use user_id here
    serializer = JudgeSerializer(instance=judge)
    return Response({"Judge": serializer.data}, status=status.HTTP_200_OK)


# Create Judge API View
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_judge(request):
    try:
        with transaction.atomic():
            user_response, judge_response = create_user_and_judge(request.data)

            # Map judge to user and contest, create sheets
            responses = [
                create_user_role_map({
                    "uuid": user_response.get("user").get("id"),
                    "role": 3,
                    "relatedid": judge_response.get("id")
                }),
                create_contest_to_judge_map({
                    "contestid": request.data["contestid"],
                    "judgeid": judge_response.get("id")
                }),
                map_cluster_to_judge({
                    "judgeid": judge_response.get("id"),
                    "clusterid": request.data["clusterid"]
                }),
                create_sheets_for_teams_in_cluster(
                    judge_response.get("id"),
                    request.data["clusterid"],
                    request.data["penalties"],
                    request.data["presentation"],
                    request.data["journal"],
                    request.data["mdo"]
                )
            ]

            # Check for any errors in mapping responses
            for response in responses:
                if isinstance(response, Response):
                    return response

            return Response({
                "user": user_response,
                "judge": judge_response,
                "user_map": responses[0],
                "contest_map": responses[1],
                "cluster_map": responses[2],
                "score_sheets": responses[3]
            }, status=status.HTTP_201_CREATED)

    except ValidationError as e:  # Catching ValidationErrors specifically
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
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
    raise ValidationError(serializer.errors)


def create_user_and_judge(data):
    user_data = {"username": data["username"], "password": data["password"]}
    user_response = create_user(user_data)
    if not user_response.get('user'):
        raise ValidationError('User creation failed.')
    judge_data = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "contestid": data["contestid"],
        "presentation": data["presentation"],
        "mdo": data["mdo"],
        "journal": data["journal"],
        "penalties": data["penalties"]
    }
    judge_response = create_judge_instance(judge_data)
    if not judge_response.get('id'):  # If judge creation fails, raise an exception
        raise ValidationError('Judge creation failed.')
    return user_response, judge_response

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def are_all_score_sheets_submitted(request, judge_id):
    """
    Check if all score sheets for a given judge are submitted.
    """
    # Filter to get all mappings for the judge
    mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=judge_id)

    if not mappings.exists():
        return Response(
            {"detail": "No score sheet mappings found for this judge."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check all score sheets for the retrieved mappings
    all_submitted = True  # Assume all are submitted until proven otherwise
    for mapping in mappings:
        sheets = Scoresheet.objects.filter(id=mapping.scoresheetid)
        if not sheets.exists():
            return Response(
                {"detail": f"No score sheets found for mapping {mapping.id}."},
                status=status.HTTP_404_NOT_FOUND
            )

        if sheets.filter(isSubmitted=False).exists():
            all_submitted = False
            break  # If any score sheet is not submitted, stop checking further

    return Response(
        {"all_submitted": all_submitted},
        status=status.HTTP_200_OK
    )