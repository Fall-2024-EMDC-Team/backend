from random import choices

from django.db import models

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
    judge_cluster = models.IntegerField()

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
    region = models.CharField(max_length=50)

class ScoresheetEnum(models.IntegerChoices):
    PRESENTATION = 1
    JOURNAL = 2
    MACHINEDESIGN = 3

class Scoresheet(models.Model):
    sheetType = models.IntegerField(choices=ScoresheetEnum.choices)
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()
    field4 = models.IntegerField()
    field5 = models.IntegerField()
    field6 = models.IntegerField()
    field7 = models.IntegerField()
    field8 = models.IntegerField()

class MapScoresheetToTeamJudge():
    teamid = models.IntegerField()
    judgeid = models.IntegerField()
    scoresheetid = models.IntegerField()
    sheetType = models.IntegerField(choices=ScoresheetEnum.choices)

class MapPenaltiesToTeamJudge():
    teamid = models.IntegerField()
    judgeid = models.IntegerField()
    scoresheetid = models.IntegerField()

class Penalties(models.Model):
    PresentationPenalties = models.IntegerField()
    MachinePenalties = models.IntegerField()
