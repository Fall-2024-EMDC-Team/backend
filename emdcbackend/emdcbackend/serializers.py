from rest_framework import serializers
from .models import Judge, Teams

class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'  # Or specify the fields you want

class TeamSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Teams
        fields = ["team_name", "school_name", "journal_score", "presentation_score", "machinedesign_score",
                  "score_penalties", "judge_cluster"]
