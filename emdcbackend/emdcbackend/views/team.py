from .Maps.MapClusterToContest import get_all_teams_cluster
from ..models import Teams, Scoresheet, MapScoresheetToTeamJudge, MapContestToTeam, MapClusterToTeam, \
    MapCoachToTeam, MapUserToRole, Coach, Judge, MapJudgeToCluster
from .coach import create_coach, create_user_and_coach, get_coach
from ..serializers import TeamSerializer, ScoresheetSerializer, CoachSerializer
from .scoresheets import create_score_sheets_for_team, make_sheets_for_team
from ..serializers import TeamSerializer
from .Maps.MapUserToRole import get_role_mapping, create_user_role_map
from .Maps.MapCoachToTeam import create_coach_to_team_map
from .Maps.MapContestToTeam import create_team_to_contest_map
from .Maps.MapClusterToTeam import create_team_to_cluster_map

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
from django.contrib.auth.models import User
from ..serializers import TeamSerializer
from .Maps.MapUserToRole import get_role_mapping, create_user_role_map
from .Maps.MapCoachToTeam import create_coach_to_team_map
from .Maps.MapContestToTeam import create_team_to_contest_map
from .Maps.MapClusterToTeam import create_team_to_cluster_map
from django.shortcuts import get_object_or_404
from django.db import transaction

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
            # Step 1: Create team object
            team_response = make_team(request.data)

            try:
                # Step 2: Retrieve user and create coach if necessary
                user = User.objects.get(username=request.data["username"])

                role_mapping_response = get_role_mapping(user.id)
                if role_mapping_response.get("id"):
                    if role_mapping_response.get("role") == 4:
                        coach_response = get_coach(role_mapping_response.get("relatedid"))
                    else:
                        raise ValidationError({"detail": "This user is already mapped to a role."})
                else:
                    coach_response = create_coach(request.data)
                    role_mapping_response = create_user_role_map({
                        "uuid": user.id,
                        "role": 4,
                        "relatedid": coach_response.get("id")
                    })
            except:
                user_response, coach_response = create_user_and_coach(request.data)
                role_mapping_response = create_user_role_map({
                    "uuid": user_response.get("user").get("id"),
                    "role": 4,
                    "relatedid": coach_response.get("id")
                })

            # Step 3: Create mapping responses
            responses = []

            # Create coach to team map
            coach_to_team_response = create_coach_to_team_map({
                "teamid": team_response.get("id"),
                "coachid": coach_response.get("id")
            })
            if isinstance(coach_to_team_response, Response):
                return coach_to_team_response
            responses.append(coach_to_team_response)

            # Create team to contest map
            team_to_contest_response = create_team_to_contest_map({
                "contestid": request.data["contestid"],
                "teamid": team_response.get("id")
            })
            if isinstance(team_to_contest_response, Response):
                return team_to_contest_response
            responses.append(team_to_contest_response)

            # Step 4: Map team to the "All Teams" cluster (default cluster)
            all_teams_cluster_id = get_all_teams_cluster(request.data["contestid"])  # Assume the "All Teams" cluster has ID = 1 (you can adjust this)
            if all_teams_cluster_id:
                create_team_to_cluster_map({
                    "clusterid": all_teams_cluster_id,
                    "teamid": team_response.get("id")
                })

            # Step 5: Check if the provided clusterid is not the "All Teams" cluster
            if request.data["clusterid"] != all_teams_cluster_id:
                # Map team to the other provided cluster
                other_cluster_mapping_response = create_team_to_cluster_map({
                    "clusterid": request.data["clusterid"],
                    "teamid": team_response.get("id")
                })
                if isinstance(other_cluster_mapping_response, Response):
                    return other_cluster_mapping_response
                responses.append(other_cluster_mapping_response)

            # Step 6: Check responses and return
            return Response({
                "team": team_response,
                "coach": coach_response,
                "coach_to_team_map": responses[0],
                "team_to_contest_map": responses[1],
                "team_to_all_teams_cluster_map": responses[2] if len(responses) > 2 else None,
                "team_to_cluster_map": responses[3] if len(responses) > 3 else None
            }, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        # Specific error handling for validation errors
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # General error handling
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_team(request):
    try:
        with transaction.atomic():
            # Retrieve team, coach, and user details
            team = get_object_or_404(Teams, id=request.data["id"])
            coach_team_mapping = get_object_or_404(MapCoachToTeam, teamid=team.id)
            coach = get_object_or_404(Coach, id=coach_team_mapping.coachid)
            mapping = MapUserToRole.objects.get(relatedid=coach.id, role=4)
            uuid = mapping.uuid
            user = get_object_or_404(User, id=uuid)

            # Update team name if necessary
            if request.data["team_name"] != team.team_name:
                team.team_name = request.data["team_name"]

            # Update coach and user mappings if username has changed
            if request.data["username"] != user.username:
                # Remove old mapping, create or fetch the user and coach, and map them to the team
                MapCoachToTeam.objects.get(teamid=team.id, coachid=coach.id).delete()
                try:
                    user = User.objects.get(username=request.data["username"])
                    role_mapping_response = get_role_mapping(user.id)
                    if role_mapping_response.get("id") and role_mapping_response.get("role") == 4:
                        coach_response = get_coach(role_mapping_response.get("relatedid"))
                    else:
                        raise ValidationError({"detail": "This user is already mapped to a role."})
                except User.DoesNotExist:
                    user_response, coach_response = create_user_and_coach(request.data)
                    create_user_role_map({
                        "uuid": user_response.get("user").get("id"),
                        "role": 4,
                        "relatedid": coach_response.get("id")
                    })
                create_coach_to_team_map({"teamid": team.id, "coachid": coach_response.get("id")})

            # Update coach details if changed
            if request.data["first_name"] != coach.first_name:
                coach.first_name = request.data["first_name"]
                coach.save()
            if request.data["last_name"] != coach.last_name:
                coach.last_name = request.data["last_name"]
                coach.save()

            # Update cluster and score sheets
            all_teams_cluster = get_all_teams_cluster(request.data["contestid"])

            new_cluster_is_all_teams = request.data["clusterid"] == get_all_teams_cluster(request.data["contestid"])

            non_all_teams_cluster_mapping = MapClusterToTeam.objects.filter(
                teamid=team.id
            ).exclude(clusterid=all_teams_cluster)

            judges_in_all_teams = MapJudgeToCluster.objects.filter(clusterid=all_teams_cluster)
            all_score_sheets_assigned_to_team = MapScoresheetToTeamJudge.objects.filter(teamid=team.id)
            non_all_teams_score_sheets = all_score_sheets_assigned_to_team.exclude(judgeid__in=judges_in_all_teams)


            if new_cluster_is_all_teams and non_all_teams_cluster_mapping:
                # New Cluster is all teams and team was assigned to other clusters previously
                non_all_teams_cluster_mapping.delete()
                scoresheets_to_delete_ids = non_all_teams_score_sheets.values_list('scoresheetid', flat=True)
                MapScoresheetToTeamJudge.objects.filter(scoresheetid__in=scoresheets_to_delete_ids).delete()
                Scoresheet.objects.filter(id__in=scoresheets_to_delete_ids).delete()
            elif not new_cluster_is_all_teams and not non_all_teams_cluster_mapping:
                # New cluster is not all teams and team wasn't assigned to other clusters previously
                create_team_to_cluster_map({"clusterid": request.data["clusterid"], "teamid": team.id})
                judge_ids = MapJudgeToCluster.objects.filter(clusterid=request.data["clusterid"]).values_list('judgeid', flat=True)
                judges = Judge.objects.filter(id__in=judge_ids)
                create_score_sheets_for_team(team, judges)
            elif not new_cluster_is_all_teams and non_all_teams_cluster_mapping:
                # New cluster is not all teams and team was assigned to other clusters previously
                non_all_teams_cluster_mapping.delete()
                create_team_to_cluster_map({"clusterid": request.data["clusterid"], "teamid": team.id})
                scoresheets_to_delete_ids = non_all_teams_score_sheets.values_list('scoresheetid', flat=True)
                MapScoresheetToTeamJudge.objects.filter(scoresheetid__in=scoresheets_to_delete_ids).delete()
                Scoresheet.objects.filter(id__in=scoresheets_to_delete_ids).delete()
                judge_ids = MapJudgeToCluster.objects.filter(clusterid=request.data["clusterid"]).values_list('judgeid',flat=True)
                judges = Judge.objects.filter(id__in=judge_ids)
                create_score_sheets_for_team(team, judges)

            team.save()
            serializer = TeamSerializer(instance=team)
            coach_serializer = CoachSerializer(instance=coach)

            score_sheet_ids = MapScoresheetToTeamJudge.objects.filter(teamid=team.id).values_list('scoresheetid', flat=True)
            score_sheets = Scoresheet.objects.filter(id__in=score_sheet_ids)
            score_sheets_data = ScoresheetSerializer(score_sheets, many=True).data

    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"Team": serializer.data, "ScoreSheets": score_sheets_data, "Coach": coach_serializer.data}, status=status.HTTP_200_OK)

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
        "penalties_score":data["penalties_score"],
        "total_score":data["total_score"]
    }
    team_response = make_team_instance(team_data)
    if not team_response.get('id'):
        raise ValidationError('Team creation failed.')
    return team_response

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication]) 
@permission_classes([IsAuthenticated])
def get_teams_by_team_rank(request):
    mappings = MapContestToTeam.objects.filter(contestid=request.data["contestid"])
    teams = Teams.objects.filter(id__in=mappings.values_list('teamid', flat=True,),team_rank__isnull=False).order_by('team_rank')
    serializer = TeamSerializer(teams, many=True)
    return Response({"Teams": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_team_after_judge(request):
  try:
    with transaction.atomic():
      # create team object.
      team_response = make_team(request.data)
      
      try:
        user = User.objects.get(username=request.data["username"])
        
        role_mapping_response = get_role_mapping(user.id)
        if role_mapping_response.get("id"):
          # if we have the mapping and it matches, we get the coach from the mapping
          if role_mapping_response.get("role") == 4:
            coach_response = get_coach(role_mapping_response.get("relatedid"))
          else:
            raise ValidationError({"detail": "This user is already mapped to a role."})
        else:
          coach_response = create_coach(request.data)
          role_mapping_response = create_user_role_map({
            "uuid": user.id,
            "role": 4,
            "relatedid": coach_response.get("id")
            })
      except:
        user_response, coach_response = create_user_and_coach(request.data)
        role_mapping_response = create_user_role_map({
            "uuid": user_response.get("user").get("id"),
            "role": 4,
            "relatedid": coach_response.get("id")
            })
        
      responses = [
        # map team to coach, map team to contest, map team to cluster, create score sheets for team
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
        make_sheets_for_team(  # create score sheets for all judges in cluster and map them
          teamid=team_response.get("id"),
          clusterid=request.data["clusterid"]
        )
      ]

      for response in responses:
        if isinstance(response, Response):
          return response
        
      return Response({
        "team":team_response,
        "coach":coach_response,
        "coach to team map": responses[0],
        "team to contest map": responses[1],
        "team to cluster map": responses[2],
        "score sheets": responses[3],
      },status=status.HTTP_201_CREATED)
    
  except ValidationError as e:  # Catching ValidationErrors specifically
    return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
  
  except Exception as e:
    return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def is_team_disqualified(request):
    team = get_object_or_404(Teams, id=request.data["teamid"])
    return Response({"is disqualified": team.organizer_disqualified}, status=status.HTTP_200_OK)
