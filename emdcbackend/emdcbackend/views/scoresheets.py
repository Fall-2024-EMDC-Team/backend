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
from .Maps.MapScoreSheet import delete_score_sheet_mapping
from ..models import Scoresheet, Teams, Judge, MapClusterToTeam, MapScoresheetToTeamJudge, MapJudgeToCluster, ScoresheetEnum
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
    scores.field9 = request.data["field9"]
    if scores.sheetType == ScoresheetEnum.PENALTIES:
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
      scores.field22 = request.data["field22"]
      scores.field23 = request.data["field23"]
      scores.field24 = request.data["field24"]
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
    scores.field9 = request.data["field9"]
    if scores.sheetType == ScoresheetEnum.PENALTIES:
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
      scores.field22 = request.data["field22"]
      scores.field23 = request.data["field23"]
      scores.field24 = request.data["field24"]
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
        "field6": 0.0,
        "field7": 0.0,
        "field8": 0.0,
        "field9": "",
        "field10": 0.0,
        "field11": 0.0,
        "field12": 0.0,
        "field13": 0.0,
        "field14": 0.0,
        "field15": 0.0,
        "field16": 0.0,
        "field17": 0.0,
        "field18": 0.0,
        "field19": 0.0,
        "field20": 0.0,
        "field21": 0.0,
        "field22": 0.0,
        "field23": 0.0,
        "field24": 0.0,
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

def get_scoresheet_id(judge_id, team_id, scoresheet_type):
    try:
        mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team_id, sheetType=scoresheet_type)
        scoresheet = Scoresheet.objects.get(id=mapping.scoresheetid)
        return scoresheet.id
    except Scoresheet.DoesNotExist:
        raise ValidationError({"error": "No scoresheet found"})
    
def delete_sheets_for_teams_in_cluster(judge_id, cluster_id, penalties, presentation, journal, mdo):
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

        for team in teams_in_cluster:
            if penalties:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, 4)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=4)
                delete_score_sheet_mapping(mapping.id)  # Delete mapping
                scoresheet.delete()  # Delete scoresheet
            if presentation:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, 1)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=1)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if journal:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, 2)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=2)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()
            if mdo:
                scoresheet_id = get_scoresheet_id(judge_id, team.id, 3)
                scoresheet = Scoresheet.objects.get(id=scoresheet_id)
                mapping = MapScoresheetToTeamJudge.objects.get(judgeid=judge_id, teamid=team.id, sheetType=3)
                delete_score_sheet_mapping(mapping.id)
                scoresheet.delete()

    except Exception as e:
        raise ValidationError({"detail": str(e)})
  
def make_sheets_for_team(teamid, clusterid):
    created_score_sheets = []
    judges = MapJudgeToCluster.objects.filter(clusterid=clusterid)  # get list of judge mappings
    for judge_map in judges:
        # Create score sheets for each type (Presentation, Journal, Machine Design, Penalties) based on the judge's role
        judge = Judge.objects.get(id=judge_map.judgeid)  # get judge from judge mapping

        if judge.presentation:
            sheet = create_base_score_sheet(1)
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.get('id'), "sheetType": 1}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({
                    "team_id": teamid,
                    "judge_id": judge.id,
                    "scoresheet_id": sheet.get('id'),
                    "sheetType": 1
                })
            else:
                raise ValidationError(map_serializer.errors)
            # score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.PRESENTATION, isSubmitted=False)
            # MapScoresheetToTeamJudge.objects.create(
            #     teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.PRESENTATION
            # )
            # created_score_sheets.append(score_sheet)
        if judge.journal:
            sheet = create_base_score_sheet(2)
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.get('id'), "sheetType": 2}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({
                    "team_id": teamid,
                    "judge_id": judge.id,
                    "scoresheet_id": sheet.get('id'),
                    "sheetType": 2
                })
            else:
                raise ValidationError(map_serializer.errors)
            # score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.JOURNAL, isSubmitted=False)
            # MapScoresheetToTeamJudge.objects.create(
            #     teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.JOURNAL
            # )
            # created_score_sheets.append(score_sheet)
        if judge.mdo:
            sheet = create_base_score_sheet(3)
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.get('id'), "sheetType": 3}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({
                    "team_id": teamid,
                    "judge_id": judge.id,
                    "scoresheet_id": sheet.get('id'),
                    "sheetType": 3
                })
            else:
                raise ValidationError(map_serializer.errors)
            # score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.MACHINEDESIGN, isSubmitted=False)
            # MapScoresheetToTeamJudge.objects.create(
            #     teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.MACHINEDESIGN
            # )
            # created_score_sheets.append(score_sheet)
        if judge.penalties:
            sheet = create_base_score_sheet_penalties()
            map_data = {"teamid": teamid, "judgeid": judge.id, "scoresheetid": sheet.get('id'), "sheetType": 4}
            map_serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
            if map_serializer.is_valid():
                map_serializer.save()
                created_score_sheets.append({
                    "team_id": teamid,
                    "judge_id": judge.id,
                    "scoresheet_id": sheet.get('id'),
                    "sheetType": 4
                })
            else:
                raise ValidationError(map_serializer.errors)
            # score_sheet = Scoresheet.objects.create(sheetType=ScoresheetEnum.PENALTIES, isSubmitted=False)
            # MapScoresheetToTeamJudge.objects.create(
            #     teamid=team.id, judgeid=judge.id, scoresheetid=score_sheet.id, sheetType=ScoresheetEnum.PENALTIES
            # )
            # created_score_sheets.append(score_sheet)

    return created_score_sheets


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication]) 
@permission_classes([IsAuthenticated]) 
def get_scoresheet_details_by_team(request):
    scoresheet_mappings = MapScoresheetToTeamJudge.objects.filter(teamid=request.data["teamid"])
    scoresheets = Scoresheet.objects.filter(id__in=scoresheet_mappings.values_list('scoresheetid', flat=True))
    presentation_scoresheet_details = [[] for _ in range(9)]
    journal_scoresheet_details = [[] for _ in range(9)]
    machinedesign_scoresheet_details = [[] for _ in range(9)]
    penalties_scoresheet_details = [[] for _ in range(24)]
    for sheet in scoresheets:
      if sheet.sheetType == 1:
        presentation_scoresheet_details[0].append(sheet.field1)
        presentation_scoresheet_details[1].append(sheet.field2)
        presentation_scoresheet_details[2].append(sheet.field3)
        presentation_scoresheet_details[3].append(sheet.field4)
        presentation_scoresheet_details[4].append(sheet.field5)
        presentation_scoresheet_details[5].append(sheet.field6)
        presentation_scoresheet_details[6].append(sheet.field7)
        presentation_scoresheet_details[7].append(sheet.field8)
        presentation_scoresheet_details[8].append(sheet.field9)
      elif sheet.sheetType == 2:
        journal_scoresheet_details[0].append(sheet.field1)
        journal_scoresheet_details[1].append(sheet.field2)
        journal_scoresheet_details[2].append(sheet.field3)
        journal_scoresheet_details[3].append(sheet.field4)
        journal_scoresheet_details[4].append(sheet.field5)
        journal_scoresheet_details[5].append(sheet.field6)
        journal_scoresheet_details[6].append(sheet.field7)
        journal_scoresheet_details[7].append(sheet.field8)
        journal_scoresheet_details[8].append(sheet.field9)
      elif sheet.sheetType == 3:
        machinedesign_scoresheet_details[0].append(sheet.field1)
        machinedesign_scoresheet_details[1].append(sheet.field2)
        machinedesign_scoresheet_details[2].append(sheet.field3)
        machinedesign_scoresheet_details[3].append(sheet.field4)
        machinedesign_scoresheet_details[4].append(sheet.field5)
        machinedesign_scoresheet_details[5].append(sheet.field6)
        machinedesign_scoresheet_details[6].append(sheet.field7)
        machinedesign_scoresheet_details[7].append(sheet.field8)
        machinedesign_scoresheet_details[8].append(sheet.field9)
      elif sheet.sheetType == 4:
        penalties_scoresheet_details[0].append(sheet.field1)
        penalties_scoresheet_details[1].append(sheet.field2)
        penalties_scoresheet_details[2].append(sheet.field3)
        penalties_scoresheet_details[3].append(sheet.field4)
        penalties_scoresheet_details[4].append(sheet.field5)
        penalties_scoresheet_details[5].append(sheet.field6)
        penalties_scoresheet_details[6].append(sheet.field7)
        penalties_scoresheet_details[7].append(sheet.field8)
        penalties_scoresheet_details[8].append(sheet.field9)
        penalties_scoresheet_details[9].append(sheet.field10)
        penalties_scoresheet_details[10].append(sheet.field11)
        penalties_scoresheet_details[11].append(sheet.field12)
        penalties_scoresheet_details[12].append(sheet.field13)
        penalties_scoresheet_details[13].append(sheet.field14)
        penalties_scoresheet_details[14].append(sheet.field15)
        penalties_scoresheet_details[15].append(sheet.field16)
        penalties_scoresheet_details[16].append(sheet.field17)
        penalties_scoresheet_details[17].append(sheet.field18)
        penalties_scoresheet_details[18].append(sheet.field19)
        penalties_scoresheet_details[19].append(sheet.field20)
        penalties_scoresheet_details[20].append(sheet.field21)
        penalties_scoresheet_details[21].append(sheet.field22)
        penalties_scoresheet_details[22].append(sheet.field23)
        penalties_scoresheet_details[23].append(sheet.field24)


    return Response({
        1: presentation_scoresheet_details,
        2: journal_scoresheet_details,
        3: machinedesign_scoresheet_details,
        4: penalties_scoresheet_details
    }, status=status.HTTP_200_OK)

