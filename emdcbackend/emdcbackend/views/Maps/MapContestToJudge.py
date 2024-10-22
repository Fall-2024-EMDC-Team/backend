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

from ...models import MapContestToJudge, Judge, Contest
from ...serializers import MapContestToJudgeSerializer, ContestSerializer, JudgeSerializer


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contest_judge_mapping(request):
    try:
        map_data = request.data
        result = create_contest_to_judge_map(map_data)
        return Response(result, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_judges_by_contest_id(request, contest_id):
    judge_ids = MapContestToJudge.objects.filter(contestid=contest_id).values_list('judgeid', flat=True)
    judges = Judge.objects.filter(id__in=judge_ids)
    serializer = JudgeSerializer(judges, many=True)
    return Response({"Judges": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_contest_id_by_judge_id(request, judge_id):
  try:
    current_map = MapContestToJudge.objects.get(judgeid=judge_id)
    contest_id = current_map.contestid
    contest = Contest.objects.get(id=contest_id)
    serializer = ContestSerializer(instance=contest)
    return Response({"Contest": serializer.data}, status=status.HTTP_200_OK)
  except MapContestToJudge.DoesNotExist:
    return Response({"There is No Contest Found for the given Judge"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contest_judge_mapping_by_id(request, map_id):
    map_to_delete = get_object_or_404(MapContestToJudge, id=map_id)
    map_to_delete.delete()
    return Response({"detail": "Contest To Judge Mapping deleted successfully."}, status=status.HTTP_200_OK)


def create_contest_to_judge_map(map_data):
    serializer = MapContestToJudgeSerializer(data=map_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)
