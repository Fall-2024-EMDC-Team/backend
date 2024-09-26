from rest_framework import serializers
from .models import Judge

class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'  # Or specify the fields you want