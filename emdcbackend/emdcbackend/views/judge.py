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
from .Maps.MapClusterToJudge import map_cluster_to_judge, cluster_by_judge_id, delete_cluster_judge_mapping_by_id
from .scoresheets import create_sheets_for_teams_in_cluster, delete_score_sheet, create_base_score_sheet, get_scoresheet_id
from ..auth.views import create_user
from ..models import Judge, Scoresheet, MapScoresheetToTeamJudge, MapJudgeToCluster, JudgeClusters
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
    try:
        judge = get_object_or_404(Judge, id=request.data["id"])
        new_first_name = request.data["first_name"]
        new_last_name = request.data["last_name"]
        new_presentation = request.data["presentation"]
        new_mdo = request.data["mdo"]
        new_journal = request.data["journal"]
        new_penalties = request.data["penalties"]
        new_cluster = request.data["clusterid"]

        with transaction.atomic():
            cluster = MapJudgeToCluster.objects.get(judgeid=judge.id)  # get cluster id from mapping
            clusterid = cluster.clusterid

            # Update judge details
            if new_first_name != judge.first_name:
                judge.first_name = new_first_name
            if new_last_name != judge.last_name:
                judge.last_name = new_last_name

            if clusterid != new_cluster:  # if the judge is being moved to a new cluster
                # Check if the judge has any scoresheets
                has_penalties, has_presentation, has_mdo, has_journal = None, None, None, None
                if judge.penalties == True:
                    has_penalties = 0
                if judge.presentation == True:
                    has_presentation = 0
                if judge.mdo == True:
                    has_mdo = 0
                if judge.journal == True:
                    has_journal = 0

                # delete all scoresheets and mappings for the judge
                Scoresheet.objects.filter(id__in=MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id).values_list('scoresheetid', flat=True)).delete()
                MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id).delete()
                
                # create new blank scoresheets
                create_sheets_for_teams_in_cluster(judge.id, new_cluster, has_penalties, has_presentation, has_mdo, has_journal)

                # delete the old cluster-judge mapping and create a new one
                delete_cluster_judge_mapping_by_id(cluster.id)
                map_cluster_to_judge({
                    "judgeid": judge.id,
                    "clusterid": new_cluster
                })
            
            # Update judge scoresheet details
            if new_presentation != judge.presentation:  # account for if getting ride of a scoresheet or adding one
                if judge.presentation == True:  # going from true to false
                    teamid = MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id).values_list('teamid', flat=True)
                    scoresheetid = get_scoresheet_id(judge.id, teamid, 1)
                    delete_score_sheet(scoresheetid)
                    judge.presentation = new_presentation
                else:
                    create_base_score_sheet("presentation")
                    judge.presentation = new_presentation
            if new_mdo != judge.mdo:
                if judge.mdo == True:  # going from true to false
                    teamid = MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id).values_list('teamid', flat=True)
                    scoresheetid = get_scoresheet_id(judge.id, teamid, 2)
                    delete_score_sheet(scoresheetid)
                    judge.mdo = new_mdo
                else:
                    create_base_score_sheet("mdo")
                    judge.mdo = new_mdo
            if new_journal != judge.journal:
                if judge.journal == True:  # going from true to false
                    teamid = MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id).values_list('teamid', flat=True)
                    scoresheetid = get_scoresheet_id(judge.id, teamid, 3)
                    delete_score_sheet(scoresheetid)
                    judge.journal = new_journal
                else:
                    create_base_score_sheet("journal")
                    judge.journal = new_journal
            if new_penalties != judge.penalties:
                if judge.penalties == True:  # going from true to false
                    teamid = MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id).values_list('teamid', flat=True)
                    scoresheetid = get_scoresheet_id(judge.id, teamid, 4)
                    delete_score_sheet(scoresheetid)
                    judge.presentation = new_penalties
                else:
                    create_base_score_sheet("penalties")
                    judge.presentation = new_penalties

            judge.save()

        serializer = JudgeSerializer(instance=judge)
    
    except Exception as e:
        raise ValidationError({"detail": str(e)})
    
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


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def are_all_score_sheets_submitted(request):
    """
    Check if all score sheets assigned to a list of judges are submitted.
    Expects a JSON body with a list of judge objects.
    """
    judges = request.data

    if not judges:
        return Response(
            {"detail": "No judges provided."},
            status=status.HTTP_400_BAD_REQUEST
        )

    results = {}

    # Iterate over each judge object in the list
    for judge in judges:
        judge_id = judge.get('id')
        # Retrieve all mappings for the judge
        mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=judge_id)

        if not mappings.exists():
            results[judge_id] = False
            continue

        # Check if all score sheets for the retrieved mappings are submitted
        all_submitted = not Scoresheet.objects.filter(
            id__in=[m.scoresheetid for m in mappings],
            isSubmitted=False
        ).exists()

        # Store the result for this judge
        results[judge_id] = all_submitted

    return Response(results, status=status.HTTP_200_OK)