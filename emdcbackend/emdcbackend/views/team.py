from ..models import Teams
from .coach import create_coach_only, create_user_and_coach, get_coach
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeamSerializer
from .Maps.MapUserToRole import get_role, get_role_mapping, create_user_role_map
from .Maps.MapCoachToTeam import create_coach_to_team_map
from .Maps.MapContestToTeam import create_team_to_contest_map
from .Maps.MapClusterToTeam import create_team_to_cluster_map
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.exceptions import ValidationError

# get team
@api_view(["GET"])
def team_by_id(request, team_id):
    team = get_object_or_404(Teams, id=team_id)
    serializer = TeamSerializer(instance=team)
    return Response({"Team": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_team(request):
    try:
        with transaction.atomic():
            # create team object.
            team_response = make_team(request.data)

            # Attempt to get user or handle if user doesn't exist
            try:
                user = User.objects.get(username=request.data["username"])
            except User.DoesNotExist:
                # Create user and coach if user does not exist
                user_response, coach_response = create_user_and_coach(request.data)
                role_mapping_response = create_user_role_map({
                    "uuid": user_response.get("user").get("id"),
                    "role": 4,
                    "relatedid": coach_response.get("id")
                })
            else:
                # if a user exists, check the user's role
                role_mapping_response = get_role_mapping(user.id)
                if role_mapping_response and role_mapping_response.get("id"):
                    # Check if user already has a coach role
                    if role_mapping_response.get("role") == 4:
                        coach_response = get_coach(role_mapping_response.get("relatedid"))
                    else:
                        raise ValidationError({"detail": "This user is already mapped to a role."})
                else:
                    # No role mapping, create a new coach
                    coach_response = create_coach_only(request.data)
                    role_mapping_response = create_user_role_map({
                        "uuid": user.id,
                        "role": 4,
                        "relatedid": coach_response.get("id")
                    })

            # Create the mappings for the team, contest, and cluster
            responses = [
                create_coach_to_team_map({
                    "teamid": team_response.get("id"),
                    "coachid": coach_response.get("id")
                }),

                create_team_to_contest_map({
                    "contestid": request.data["contestid"],
                    "teamid": team_response.get("id")
                }),

                create_team_to_cluster_map({
                    "clusterid": request.data["clusterid"],
                    "teamid": team_response.get("id")
                }),

                role_mapping_response
            ]

            for response in responses:
                if isinstance(response, Response):
                    return response

            return Response({
                "team": team_response,
                "coach": coach_response,
                "coach to team map": responses[0],
                "team to contest map": responses[1],
                "team to cluster map": responses[2],
                "user to coach mapping" : responses[3]
            }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# edit team
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_team(request):
    team = get_object_or_404(Teams, id=request.data["id"])
    team.team_name = request.data["team_name"]
    team.journal_score = request.data["journal_score"]
    team.presentation_score = request.data["presentation_score"]
    team.machinedesign_score = request.data["machinedesign_score"]
    team.score_penalties = request.data["score_penalties"]
    team.judge_cluster = request.data["judge_cluster"]
    team.save()

    serializer = TeamSerializer(instance=team)
    return Response({"team": serializer.data})

# delete team
@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_team_by_id(request, team_id):
    team_to_delete = get_object_or_404(Teams, id=team_id)
    team_to_delete.delete()
    return Response({"detail": "Team deleted successfully."}, status=status.HTTP_200_OK)

def make_team_instance(team_data):
    serializer = TeamSerializer(data=team_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise ValidationError(serializer.errors)

def make_team(data):
    team_data = {
        "team_name":data["team_name"],
        "journal_score":data["journal_score"],
        "presentation_score":data["presentation_score"],
        "machinedesign_score":data["machinedesign_score"],
        "score_penalties":data["score_penalties"]
    }
    team_response = make_team_instance(team_data)
    if not team_response.get('id'):
        raise ValidationError('Team creation failed.')
    return team_response



