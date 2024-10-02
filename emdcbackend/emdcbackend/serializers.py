from rest_framework import serializers
from .models import Judge, Organizer, Contest, Coach, MapCoachToTeam, Scoresheet, JudgeClusters, MapContestToJudge, MapContestToOrganizer, MapContestToTeam, MapUserToRole
from .models import Teams

class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'  # Or specify the fields you want

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'

class CoachToTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapCoachToTeam
        fields = '__all__'

class MapContestToOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapContestToOrganizer
        fields = '__all__'

class MapContestToTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapContestToTeam
        fields = '__all__'

class MapContestToJudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapContestToJudge
        fields = '__all__'

class JudgeClustersSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeClusters
        fields = '__all__'

class ScoresheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scoresheet
        fields = '__all__'

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'

class MapUserToRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapUserToRole
        fields = '__all__'