from rest_framework import serializers
from .models import Judge, Organizer, Contest, Coach, MapCoachToTeam, MachineDesignScores, JournalScores, PresentationScores


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

class MachineDesignScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineDesignScores
        fields = '__all__'

class JournalScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalScores
        fields = '__all__'

class PresentationScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationScores
        fields = '__all__'
