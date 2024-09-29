from rest_framework import serializers
from .models import Judge, Organizer, Contest, MapContestToJudge

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

class MapContestToJudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapContestToJudge
        fields = '__all__'