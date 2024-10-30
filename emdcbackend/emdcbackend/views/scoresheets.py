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
from rest_framework.exceptions import ValidationError

from ..models import Scoresheet, Teams, MapClusterToTeam, MapScoresheetToTeamJudge, ScoresheetEnum
from ..serializers import ScoresheetSerializer, MapScoreSheetToTeamJudgeSerializer


@api_view(["GET"])
def scores_by_id(request, scores_id):
    scores = get_object_or_404(Scoresheet, id=scores_id)
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"ScoreSheet": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_score_sheet(request):
    map_data = request.data
    result = create_score_sheet_helper(map_data)
    if "errors" in result:
        return Response(result["errors"], status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_score_sheet(request):
    scores = get_object_or_404(Scoresheet, id=request.data["id"])
    scores.sheetType = request.data["sheetType"]
    scores.isSubmitted = request.data["isSubmitted"]
    scores.field1 = request.data["field1"]
    scores.field2 = request.data["field2"]
    scores.field3 = request.data["field3"]
    scores.field4 = request.data["field4"]
    scores.field5 = request.data["field5"]
    scores.field6 = request.data["field6"]
    scores.field7 = request.data["field7"]
    scores.field8 = request.data["field8"]
    if scores.sheet_type == ScoresheetEnum.PENALTIES:
      scores.field9 = request.data["field9"]
      scores.field10 = request.data["field10"]
      scores.field11 = request.data["field11"]
      scores.field12 = request.data["field12"]
      scores.field13 = request.data["field13"]
      scores.field14 = request.data["field14"]
      scores.field15 = request.data["field15"]
      scores.field16 = request.data["field16"]
      scores.field17 = request.data["field17"]
      scores.field18 = request.data["field18"]
      scores.field19 = request.data["field19"]
      scores.field20 = request.data["field20"]
      scores.field21 = request.data["field21"]
    scores.save()
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"edit_score_sheets": serializer.data})

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_scores(request):
    scores = get_object_or_404(Scoresheet, id=request.data["id"])
    scores.field1 = request.data["field1"]
    scores.field2 = request.data["field2"]
    scores.field3 = request.data["field3"]
    scores.field4 = request.data["field4"]
    scores.field5 = request.data["field5"]
    scores.field6 = request.data["field6"]
    scores.field7 = request.data["field7"]
    scores.field8 = request.data["field8"]
    scores.fieldText = request.data["fieldText"]
    if scores.sheet_type == ScoresheetEnum.PENALTIES:
      scores.field9 = request.data["field9"]
      scores.field10 = request.data["field10"]
      scores.field11 = request.data["field11"]
      scores.field12 = request.data["field12"]
      scores.field13 = request.data["field13"]
      scores.field14 = request.data["field14"]
      scores.field15 = request.data["field15"]
      scores.field16 = request.data["field16"]
      scores.field17 = request.data["field17"]
      scores.field18 = request.data["field18"]
      scores.field19 = request.data["field19"]
      scores.field20 = request.data["field20"]
      scores.field21 = request.data["field21"]
    scores.save()
    serializer = ScoresheetSerializer(instance=scores)
    return Response({"updated_sheet": serializer.data})

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_score_sheet_field(request):
    sheet = get_object_or_404(Scoresheet, id=request.data["id"])

    field_name = ""
    if isinstance(request.data["field"], int):
        field_name = "field"+str(request.data["field"])
    else:
        field_name = request.data["field"]

    if hasattr(sheet, field_name):
        setattr(sheet, field_name, request.data["new_value"])
        sheet.save()
        serializer = ScoresheetSerializer(instance=sheet)
        return Response({"score_sheet": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid field"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_score_sheet(request, scores_id):
    scores = get_object_or_404(Scoresheet, id=scores_id)
    scores.delete()
    return Response({"detail": "Score Sheet deleted successfully."}, status=status.HTTP_200_OK)

def create_score_sheet_helper(map_data):
    serializer = ScoresheetSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return {"errors": serializer.errors}


def create_base_score_sheet(sheet_type):
    base_score_data = {
        "sheetType": sheet_type,
        "isSubmitted": False,
        "field1": 0.0,
        "field2": 0.0,
        "field3": 0.0,
        "field4": 0.0,
        "field5": 0.0,
        "field6": 0.0,
        "field7": 0.0,
        "field8": 0.0,
        "field9": "",
    }

    serializer = ScoresheetSerializer(data=base_score_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)

def create_base_score_sheet_penalties():
    base_score_data = {
        "sheetType": 4,
        "isSubmitted": False,
        "field1": 0.0,
        "field2": 0.0,
        "field3": 0.0,
        "field4": 0.0,
        "field5": 0.0,
        "field6": 0.0
    }

    serializer = ScoresheetSerializer(data=base_score_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)

def create_sheets_for_teams_in_cluster(judge_id, cluster_id, penalties, presentation, journal, mdo):
    try:
        # Fetch all mappings for the teams in the cluster
        mappings = MapClusterToTeam.objects.filter(clusterid=cluster_id)

        # Check if mappings exist
        if not mappings.exists():
            raise ValidationError("No teams found for the specified cluster.")  # Raise an exception here

        # Extract all the team_ids from the mappings
        team_ids = mappings.values_list('teamid', flat=True)

        # Fetch all teams with the given team_ids
        teams_in_cluster = Teams.objects.filter(id__in=team_ids)

        # List to store responses
        created_score_sheets = []

        for team in teams_in_cluster:
            if penalties:
                sheet = create_base_score_sheet_penalties()
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.get('id'), "sheetType": 4}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({
                        "team_id": team.id,
                        "judge_id": judge_id,
                        "scoresheet_id": sheet.get('id'),
                        "sheetType": 4
                    })
                else:
                    raise ValidationError(map_serializer.errors)
            if presentation:
                sheet = create_base_score_sheet(1)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.get('id'), "sheetType": 1}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({
                        "team_id": team.id,
                        "judge_id": judge_id,
                        "scoresheet_id": sheet.get('id'),
                        "sheetType": 1
                    })
                else:
                    raise ValidationError(map_serializer.errors)
            if journal:
                sheet = create_base_score_sheet(2)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.get('id'), "sheetType": 2}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({
                        "team_id": team.id,
                        "judge_id": judge_id,
                        "scoresheet_id": sheet.get('id'),
                        "sheetType": 2
                    })
                else:
                    raise ValidationError(map_serializer.errors)
            if mdo:
                sheet = create_base_score_sheet(3)
                map_data = {"teamid": team.id, "judgeid": judge_id, "scoresheetid": sheet.get('id'), "sheetType": 3}
                map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
                if map_serializer.is_valid():
                    map_serializer.save()
                    created_score_sheets.append({
                        "team_id": team.id,
                        "judge_id": judge_id,
                        "scoresheet_id": sheet.get('id'),
                        "sheetType": 3
                    })
                else:
                    raise ValidationError(map_serializer.errors)

        return created_score_sheets

    except Exception as e:
        raise ValidationError({"detail": str(e)})

# Scoresheet for team
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_score_sheets_for_team(team, judges):
    created_score_sheets = []
    for judge in judges:
        # Create score sheets for each type (Presentation, Journal, Machine Design, Penalties) based on the judge's role
        if judge.presentation:
            score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.PRESENTATION, isSubmitted=False)
            MapScoresheetToTeamJudge.objects.create(
                teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.PRESENTATION
            )
            created_score_sheets.append(score_sheet)
        if judge.journal:
            score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.JOURNAL, isSubmitted=False)
            MapScoresheetToTeamJudge.objects.create(
                teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.JOURNAL
            )
            created_score_sheets.append(score_sheet)
        if judge.mdo:
            score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.MACHINEDESIGN, isSubmitted=False)
            MapScoresheetToTeamJudge.objects.create(
                teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.MACHINEDESIGN
            )
            created_score_sheets.append(score_sheet)
        if judge.penalties:
            score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.PENALTIES, isSubmitted=False)
            MapScoresheetToTeamJudge.objects.create(
                teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.PENALTIES
            )
            created_score_sheets.append(score_sheet)
        return created_score_sheets
