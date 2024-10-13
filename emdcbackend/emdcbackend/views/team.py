from ..models import Teams
from .coach import create_coach, create_user_and_coach, get_coach
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

# create team and assosciated mappings
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_team(request):
  try:
    with transaction.atomic():
      # create team object.
      team_response = make_team(request.data)
      
      # check if a user relating to the email passed in through the request exists, if it does exist, check if it has a role on it.
      user = User.objects.get(email__exact=request.data["email"])
      # if a user exists with said email, we go to check the user's role
      if user:
        # check if mapping exists, 
        role_mapping_response = get_role_mapping(user.id)
        if role_mapping_response:
          # if we have the mapping and it matches, we get the coach from the mapping
          if role_mapping_response.get("role") == 4:
            coach_response = get_coach(userMapping.get("relatedid"))
          else:
            raise ValidationError({"detail": "This user is already mapped to a role."})
        else:
          coach_response = create_coach(request.data)
          role_mapping_response = create_user_role_map({
            "uuid": user.get("id"),
            "role": 4,
            "relatedid": judge_response.get("id")
            })
      else:
        user_response, coach_response = create_user_and_coach(request.data)
        role_mapping_response = create_user_role_map({
            "uuid": user_response.get("user").get("id"),
            "role": 4,
            "relatedid": judge_response.get("id")
            })
      
      responses = [
        # map team to coach, map team to contest, map team to cluster
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
        })
      ]

      for response in responses:
          if isinstance(response, Response):
              return response

      return Response({
        "team":team_response,
        "coach":coach_response,
        "coach to team map": responses[0],
        "team to contest map": responses[1],
        "team to cluster map": responses[2]
      },status=status.HTTP_201_CREATED)
        
  except ValidationError as e:  # Catching ValidationErrors specifically
    return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  except Exception as e:
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



