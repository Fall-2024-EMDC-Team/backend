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
from ...models import MapScoresheetToTeamJudge, Scoresheet
from ...serializers import MapScoreSheetToTeamJudgeSerializer


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
def score_sheets_by_judge_team(request, judge_id, team_id):
    mappings = MapScoresheetToTeamJudge.objects.filter(judgeid = judge_id , teamid = team_id)
    sheet_ids = mappings.values_list('scoresheetid', flat=True)
    sheets = Scoresheet.objects.filter(id__in=sheet_ids)

    serializer = MapScoreSheetToTeamJudgeSerializer(sheets, many=True)

    return Response({"ScoreSheets": serializer.data}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_score_sheet_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapScoreSheetToTeamJudgeSerializer, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Mapping deleted successfully."}, status=status.HTTP_200_OK)


def map_score_sheet(map_data):
    serializer = MapScoreSheetToTeamJudgeSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data

    raise ValidationError(serializer.errors)