from random import choices

from django.db import models
from rest_framework.exceptions import ValidationError


class Contest(models.Model):
    name = models.CharField(max_length=99)
    date = models.DateField()
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
    class JudgeRoleEnum(models.IntegerChoices):
        LEAD = 1
        TECHNICAL = 2
        GENERAL = 3
        JOURNAL = 4
    
    first_name = models.CharField(max_length=50)  # Add max_length
    last_name = models.CharField(max_length=50)   # Add max_length
    phone_number = models.CharField(max_length=20)
    contestid = models.IntegerField()
    presentation=models.BooleanField()
    mdo=models.BooleanField()
    journal=models.BooleanField()
    runpenalties=models.BooleanField()
    otherpenalties=models.BooleanField()
    role = models.IntegerField(choices=JudgeRoleEnum.choices, null=True, blank=True)

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
    penalties_score = models.FloatField()
    total_score = models.FloatField()
    team_rank = models.IntegerField(null=True,blank=True)
    cluster_rank = models.IntegerField(null=True,blank=True)
    judge_disqualified = models.BooleanField(default=False)
    organizer_disqualified = models.BooleanField(default=False)

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
    RUNPENALTIES = 4
    OTHERPENALTIES = 5

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
    field10 = models.FloatField(null=True, blank=True)
    field11 = models.FloatField(null=True, blank=True)
    field12 = models.FloatField(null=True, blank=True)
    field13 = models.FloatField(null=True, blank=True)
    field14 = models.FloatField(null=True, blank=True)
    field15 = models.FloatField(null=True, blank=True)
    field16 = models.FloatField(null=True, blank=True)
    field17 = models.FloatField(null=True, blank=True)
    
    
    
    def clean(self):
        if self.sheetType == ScoresheetEnum.RUNPENALTIES:
            required_fields = {
                'field1': 'Field 1 is required for PENALTIES.',
                'field2': 'Field 2 is required for PENALTIES.',
                'field3': 'Field 3 is required for PENALTIES.',
                'field4': 'Field 4 is required for PENALTIES.',
                'field5': 'Field 5 is required for PENALTIES.',
                'field6': 'Field 6 is required for PENALTIES.',
                'field7': 'Field 7 is required for PENALTIES.',
                'field8': 'Field 8 is required for PENALTIES.',
                'field10': 'Field 10 is required for PENALTIES.',
                'field11': 'Field 11 is required for PENALTIES.',
                'field12': 'Field 12 is required for PENALTIES.',
                'field13': 'Field 13 is required for PENALTIES.',
                'field14': 'Field 14 is required for PENALTIES.',
                'field15': 'Field 15 is required for PENALTIES.',
                'field16': 'Field 16 is required for PENALTIES.',
                'field17': 'Field 17 is required for PENALTIES.',
            }

            errors = {}
            for field, error_message in required_fields.items():
                if getattr(self, field) is None:
                    errors[field] = error_message

            if errors:
                raise ValidationError(errors)
        elif self.sheetType == ScoresheetEnum.OTHERPENALTIES:
            required_fields = ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7']
            for field in required_fields:
                if getattr(self, field) is None:
                    raise ValidationError({field: f'{field.capitalize()} is required.'})
        else:
            # For other types (Presentation, Journal, Machine Design), fields 1-8 must be filled
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


    