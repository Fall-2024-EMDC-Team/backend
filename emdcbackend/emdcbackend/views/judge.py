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
from django.contrib.auth.models import User
from .Maps.MapUserToRole import create_user_role_map
from .Maps.MapContestToJudge import create_contest_to_judge_map
from .Maps.MapClusterToJudge import map_cluster_to_judge,  delete_cluster_judge_mapping
from .scoresheets import create_sheets_for_teams_in_cluster, delete_sheets_for_teams_in_cluster
from ..auth.views import create_user
from ..models import Judge, Scoresheet, MapScoresheetToTeamJudge, MapJudgeToCluster, Teams, MapContestToJudge, MapUserToRole
from ..serializers import JudgeSerializer
from ..auth.serializers import UserSerializer


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
                    request.data["presentation"],
                    request.data["journal"],
                    request.data["mdo"],
                    request.data["runpenalties"],
                    request.data["otherpenalties"],
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
        new_phone_number = request.data["phone_number"]
        new_presentation = request.data["presentation"]
        new_mdo = request.data["mdo"]
        new_journal = request.data["journal"]
        new_runpenalties = request.data["runpenalties"]
        new_otherpenalties = request.data["otherpenalties"]
        new_cluster = request.data["clusterid"]
        new_username = request.data["username"]
        new_role = request.data["role"]
        with transaction.atomic():
            cluster = MapJudgeToCluster.objects.get(judgeid=judge.id)  # get cluster id from mapping
            clusterid = cluster.clusterid
            user_mapping = MapUserToRole.objects.get(role=3, relatedid=judge.id)
            user = get_object_or_404(User, id=user_mapping.uuid)
            if user.username != new_username:
                user.username = new_username
                user.save()
            user_serializer = UserSerializer(instance=user)
            # Update judge name details
            if new_first_name != judge.first_name:
                judge.first_name = new_first_name
            if new_last_name != judge.last_name:
                judge.last_name = new_last_name
            if new_phone_number != judge.phone_number:
                judge.phone_number = new_phone_number
            if new_role != judge.role:
                judge.role = new_role

            # if the judge is being moved to a new cluster
            if clusterid != new_cluster:
                # delete all scoresheets and mappings for the judge
                delete_sheets_for_teams_in_cluster(judge.id, clusterid, judge.penalties, judge.presentation, judge.journal, judge.mdo)

                # create new blank scoresheets
                create_sheets_for_teams_in_cluster(judge.id, new_cluster, new_runpenalties, new_presentation, new_journal, new_mdo)

                # delete the old cluster-judge mapping and create a new one
                delete_cluster_judge_mapping(cluster.id)
                map_cluster_to_judge({
                    "judgeid": judge.id,
                    "clusterid": new_cluster
                })

                # update the boolean values
                if judge.presentation != new_presentation:
                    judge.presentation = new_presentation
                if judge.mdo != new_mdo:
                    judge.mdo = new_mdo
                if judge.journal != new_journal:
                    judge.journal = new_journal
                if judge.runpenalties != new_runpenalties:
                    judge.runpenalties = new_runpenalties
                if judge.otherpenalties != new_otherpenalties:
                    judge.otherpenalties = new_otherpenalties

                clusterid = new_cluster

            else:
                # if adding or removing scoresheets (no cluster change)
                if new_presentation != judge.presentation and new_presentation == False:
                        delete_sheets_for_teams_in_cluster(judge.id, clusterid, True, False, False, False, False)
                        judge.presentation = False
                elif new_presentation != judge.presentation and new_presentation == True:
                        create_sheets_for_teams_in_cluster(judge.id, clusterid, True, False, False, False, False)
                        judge.presentation = True

                if new_journal != judge.journal and new_journal == False:
                        delete_sheets_for_teams_in_cluster(judge.id, clusterid, False, True, False, False, False)
                        judge.journal = False
                elif new_journal != judge.journal and new_journal == True:
                        create_sheets_for_teams_in_cluster(judge.id, clusterid, False, True, False, False, False)
                        judge.journal = True

                if new_mdo != judge.mdo and new_mdo == False:
                        delete_sheets_for_teams_in_cluster(judge.id, clusterid, False, False, True, False, False)
                        judge.mdo = False
                elif new_mdo != judge.mdo and new_mdo == True:
                        create_sheets_for_teams_in_cluster(judge.id, clusterid, False, False, True, False, False)
                        judge.mdo = True

                if new_runpenalties != judge.runpenalties and new_runpenalties == False:
                        delete_sheets_for_teams_in_cluster(judge.id, clusterid, False, False, False, True, False)
                        judge.runpenalties = False
                elif new_runpenalties != judge.runpenalties and new_runpenalties == True:
                        create_sheets_for_teams_in_cluster(judge.id, clusterid, False, False, False, True, False)
                        judge.runpenalties = True

                if new_otherpenalties != judge.otherpenalties and new_otherpenalties == False:
                        delete_sheets_for_teams_in_cluster(judge.id, clusterid, False, False, False, False, True)
                        judge.otherpenalties = False
                elif new_otherpenalties != judge.otherpenalties and new_otherpenalties == True:
                        create_sheets_for_teams_in_cluster(judge.id, clusterid, False, False, False, False, True)
                        judge.otherpenalties = True



            judge.save()

        serializer = JudgeSerializer(instance=judge)
    
    except Exception as e:
        raise ValidationError({"detail": str(e)})
    
    return Response({"judge": serializer.data, "clusterid": clusterid, "user": user_serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_judge(request, judge_id):
    try:
        judge = get_object_or_404(Judge, id=judge_id)
        scoresheet_mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=judge_id)
        scoresheet_ids = scoresheet_mappings.values_list('scoresheetid', flat=True)
        scoresheets = Scoresheet.objects.filter(id__in=scoresheet_ids)
        user_mapping = MapUserToRole.objects.get(role=3, relatedid=judge_id)
        user = get_object_or_404(User, id=user_mapping.uuid)
        cluster_mapping = MapJudgeToCluster.objects.get(judgeid=judge_id)
        teams_mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=judge_id)
        contest_mapping = MapContestToJudge.objects.filter(judgeid=judge_id)
        # scoresheet_team_judge = MapScoresheetToTeamJudge.objects.filter(judgeid=judge_id)

        # delete associataed user
        user.delete()
        user_mapping.delete()

        # delete associated scoresheets
        for scoresheet in scoresheets:
            scoresheet.delete()

        # delete associated judge-teams mappings
        for mapping in teams_mappings:
            mapping.delete()

        # delete associated judge-contest mapping
        contest_mapping.delete()

        # delete associated judge-cluster mapping
        cluster_mapping.delete()

        # delete the judge
        judge.delete()

        return Response({"detail": "Judge deleted successfully."}, status=status.HTTP_200_OK)
    
    except ValidationError as e:  # Catching ValidationErrors specifically
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        "phone_number": data["phone_number"],
        "contestid": data["contestid"],
        "presentation": data["presentation"],
        "mdo": data["mdo"],
        "journal": data["journal"],
        "runpenalties": data["runpenalties"],
        "otherpenalties": data["otherpenalties"],
        "role": data["role"]
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

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def judge_disqualify_team(request):
     team = get_object_or_404(Teams, id=request.data["teamid"])
     team.judge_disqualified = request.data["judge_disqualified"]
     team.save()
     return Response(status=status.HTTP_200_OK)
