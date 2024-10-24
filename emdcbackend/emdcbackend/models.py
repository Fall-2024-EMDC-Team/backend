from random import choices

from django.db import models
from rest_framework.exceptions import ValidationError


class Contest(models.Model):
    name = models.CharField(max_length=99)
    is_open = models.BooleanField()
    is_tabulated = models.BooleanField()

class MapContestToJudge(models.Model):
    contestid = models.IntegerField()
    judgeid = models.IntegerField()

class MapContestToTeam(models.Model):
    contestid = models.IntegerField()
    teamid = models.IntegerField()

class MapContestToOrganizer(models.Model):
    contestid = models.IntegerField()
    organizerid = models.IntegerField()

class MapContestToCluster(models.Model):
    contestid = models.IntegerField()
    clusterid = models.IntegerField()

class Judge(models.Model):
    first_name = models.CharField(max_length=50)  # Add max_length
    last_name = models.CharField(max_length=50)   # Add max_length
    contestid = models.IntegerField()
    presentation=models.BooleanField()
    mdo=models.BooleanField()
    journal=models.BooleanField()
    penalties=models.BooleanField()

class MapJudgeToCluster(models.Model):
    judgeid = models.IntegerField()
    clusterid = models.IntegerField()

class JudgeClusters(models.Model):
    cluster_name = models.CharField(max_length=50)  # Add max_length

class MapClusterToTeam(models.Model):
    clusterid = models.IntegerField()
    teamid = models.IntegerField()

class Teams(models.Model):
    team_name = models.CharField(max_length=99)
    journal_score = models.FloatField()
    presentation_score = models.FloatField()
    machinedesign_score = models.FloatField()
    score_penalties = models.FloatField()

class MapUserToRole(models.Model):
    class RoleEnum(models.IntegerChoices):
        ADMIN = 1
        ORGANIZER = 2
        JUDGE = 3
        COACH = 4
    
    role = models.IntegerField(choices=RoleEnum.choices)
    uuid = models.IntegerField()
    relatedid = models.IntegerField()

class Coach(models.Model):
    first_name = models.CharField(max_length=50)  # Add max_length
    last_name = models.CharField(max_length=50)   # Add max_length

class Admin(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class MapCoachToTeam(models.Model):
    teamid = models.IntegerField()
    coachid = models.IntegerField()

class Organizer(models.Model):
    first_name = models.CharField(max_length=50)  # Add max_length
    last_name = models.CharField(max_length=50)   # Add max_length



class ScoresheetEnum(models.IntegerChoices):
    PRESENTATION = 1
    JOURNAL = 2
    MACHINEDESIGN = 3
    PENALTIES = 4

class Scoresheet(models.Model):
    sheetType = models.IntegerField(choices=ScoresheetEnum.choices)
    isSubmitted = models.BooleanField()
    field1 = models.FloatField(null=True, blank=True)
    field2 = models.FloatField(null=True, blank=True)
    field3 = models.FloatField(null=True, blank=True)
    field4 = models.FloatField(null=True, blank=True)
    field5 = models.FloatField(null=True, blank=True)
    field6 = models.FloatField(null=True, blank=True)
    field7 = models.FloatField(null=True, blank=True)
    field8 = models.FloatField(null=True, blank=True)
    field9 = models.CharField(null=True, blank=True, max_length=500)

    def clean(self):
        # Custom validation logic
        if self.sheetType == ScoresheetEnum.PENALTIES:
            # For PENALTIES, only field1 and field2 are required
            if self.field1 is None:
                raise ValidationError({'field1': 'Field 1 is required for PENALTIES.'})
            if self.field2 is None:
                raise ValidationError({'field2': 'Field 2 is required for PENALTIES.'})
            if self.field3 is None:
                raise ValidationError({'field2': 'Field 2 is required for PENALTIES.'})
            if self.field4 is None:
                raise ValidationError({'field2': 'Field 2 is required for PENALTIES.'})
            if self.field5 is None:
                raise ValidationError({'field2': 'Field 2 is required for PENALTIES.'})
            if self.field6 is None:
                raise ValidationError({'field2': 'Field 2 is required for PENALTIES.'})
        else:
            # For other types (Presentation, Journal, Machine Design), all fields must be filled
            required_fields = ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'field8']
            for field in required_fields:
                if getattr(self, field) is None:
                    raise ValidationError({field: f'{field.capitalize()} is required.'})

    def save(self, *args, **kwargs):
        # Call the clean method before saving to trigger validation
        self.clean()
        super().save(*args, **kwargs)

class MapScoresheetToTeamJudge(models.Model):
    teamid = models.IntegerField()
    judgeid = models.IntegerField()
    scoresheetid = models.IntegerField()
    sheetType = models.IntegerField(choices=ScoresheetEnum.choices)

class MapUserToCoach(models.Model):
    uuid = models.IntegerField()
    coachid = models.IntegerField()
    role = 4
    
class MapUserToOrganizer(models.Model):
    uuid = models.IntegerField()
    organizerid = models.IntegerField()
    role = 2

class User(models.Model):
    uuid = models.IntegerField()
    first_name = models.CharField(max_length=50)  # Add max_length
    last_name = models.CharField(max_length=50)   # Add max_length

    