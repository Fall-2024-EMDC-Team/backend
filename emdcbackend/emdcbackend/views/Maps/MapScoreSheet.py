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
from ...models import MapScoresheetToTeamJudge, Scoresheet, MapContestToJudge, MapJudgeToCluster
from ...serializers import MapScoreSheetToTeamJudgeSerializer, ScoresheetSerializer


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_score_sheet_mapping(request):
    try:
        result = map_score_sheet(request.data)
        return Response(result, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def score_sheet_by_judge_team(request, judge_id, team_id, sheetType):
    try:
        mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team_id, sheetType=sheetType)
        sheet = Scoresheet.objects.get(id=mapping.scoresheetid)
        serializer = ScoresheetSerializer(instance=sheet)
        return Response({"ScoreSheet": serializer.data}, status=status.HTTP_200_OK)

    except MapScoresheetToTeamJudge.DoesNotExist:
        return Response({"error": "No mapping found for the provided judge, team, and sheet type."},
                        status=status.HTTP_404_NOT_FOUND)

    except Scoresheet.DoesNotExist:
        return Response({"error": "Scoresheet not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def score_sheets_by_judge(request, judge_id):
    try:
        # Fetch mappings for the given judge
        mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=judge_id)

        if not mappings.exists():
            return Response({"error": "No mappings found for the provided judge."},
                            status=status.HTTP_404_NOT_FOUND)

        # Prepare data to return mappings with scoresheets
        results = []
        for mapping in mappings:
            # Fetch the scoresheet by its ID
            try:
                score_sheet = Scoresheet.objects.get(id=mapping.scoresheetid)
                serializer = ScoresheetSerializer(score_sheet).data
                total_score = 0
                if mapping.sheetType == 4:
                    total_score = (serializer.get("field1") + serializer.get("field2") + serializer.get("field3") +
                           serializer.get("field4") + serializer.get("field5") + serializer.get("field6") +
                           serializer.get("field7") + serializer.get("field8") + serializer.get("field10") +
                           serializer.get("field11") + serializer.get("field12") + serializer.get("field13") +
                           serializer.get("field14") + serializer.get("field15") + serializer.get("field16") +
                           serializer.get("field17"))
                elif mapping.sheetType == 5:
                    total_score = (serializer.get("field1") + serializer.get("field2") + serializer.get("field3") +
                                   serializer.get("field4") + serializer.get("field5") + serializer.get("field6") +
                                   serializer.get("field7"))
                else:
                    total_score = (serializer.get("field1")+serializer.get("field2")+serializer.get("field3")+
                                  serializer.get("field4")+serializer.get("field5")+serializer.get("field6")+
                                  serializer.get("field7")+serializer.get("field8"))
                results.append({
                    "mapping": {
                        "teamid": mapping.teamid,
                        "judgeid": mapping.judgeid,
                        "scoresheetid": mapping.scoresheetid,
                        "sheetType": mapping.sheetType,
                    },
                    "scoresheet": serializer,  # Serialize the scoresheet
                    "total": total_score
                })
            except Scoresheet.DoesNotExist:
                results.append({
                    "mapping": {
                        "teamid": mapping.teamid,
                        "judgeid": mapping.judgeid,
                        "scoresheetid": mapping.scoresheetid,
                        "sheetType": mapping.sheetType,
                    },
                    "scoresheet": None  # Or handle this case as needed
                })

        return Response({"ScoreSheets": results}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_sheets_submitted_for_contests(request):
    contests = request.data
    results = {}

    try:
        for contest in contests:
            contest_id = contest.get('id')
            judges = MapContestToJudge.objects.filter(contestid=contest_id)
            all_submitted = True

            for judge in judges:
                score_sheet_mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=judge.id)

                for mapping in score_sheet_mappings:
                    score_sheet = Scoresheet.objects.get(id=mapping.scoresheetid)
                    serializer = ScoresheetSerializer(score_sheet).data

                    if not serializer.get("isSubmitted"):
                        all_submitted = False
                        break

                if not all_submitted:
                    break

            results[contest_id] = all_submitted

        return Response(results, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_all_penalty_sheets_for_judge(request):
    try:
        penalty_mappings = MapScoresheetToTeamJudge.objects.filter(judgeid=request.data["judge_id"], sheetType=4)

        if not penalty_mappings.exists():
            return Response({"error": "No penalty score sheets found for the provided judge."},
                            status=status.HTTP_404_NOT_FOUND)

        for mapping in penalty_mappings:
            scoresheet = get_object_or_404(Scoresheet, id=mapping.scoresheetid)

            scoresheet.isSubmitted = True
            scoresheet.save()

        return Response(status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_score_sheet_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapScoresheetToTeamJudge, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Mapping deleted successfully."}, status=status.HTTP_200_OK)


def delete_score_sheet_mapping(map_id):
    # python can't overload functions >:(
    map_to_delete = get_object_or_404(MapScoresheetToTeamJudge, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Mapping deleted successfully."}, status=status.HTTP_200_OK)


def map_score_sheet(map_data):
    serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data

    raise ValidationError(serializer.errors)


def map_score_sheets_for_team_in_cluster(team_id, cluster_id):
    # Fetch judges assigned to the cluster
    mappings = MapJudgeToCluster.objects.filter(clusterid=cluster_id)
    judge_ids = mappings.values_list('judgeid', flat=True)

    # Fetch scoresheets assigned to the team
    team_judge_mappings = MapScoresheetToTeamJudge.objects.filter(teamid=team_id, judgeid__in=judge_ids)
    scoresheet_ids = team_judge_mappings.values_list('scoresheetid', flat=True)

    # Fetch scoresheets for the team
    scoresheets = Scoresheet.objects.filter(id__in=scoresheet_ids)
    serializer = ScoresheetSerializer(scoresheets, many=True)

    return serializer.data