from rest_framework import serializers
from .models import Judge, Organizer

class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'  # Or specify the fields you want

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'  