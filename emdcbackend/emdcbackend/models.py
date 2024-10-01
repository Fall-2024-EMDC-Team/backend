from django.db import models

class Contest(models.Model):
    name = models.CharField(max_length=99)
    is_open = models.BooleanField()
    is_tabulated = models.BooleanField()

class MapContestToJudge(models.Model):
    contestid = models.IntegerField()
    judegeid = models.IntegerField()

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
    judegeid = models.IntegerField()
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
    school_name = models.CharField(max_length=99) # Add max_length

class MapCoachToTeam(models.Model):
    teamid = models.IntegerField()
    coachid = models.IntegerField()

class Organizer(models.Model):
    first_name = models.CharField(max_length=50)  # Add max_length
    last_name = models.CharField(max_length=50)   # Add max_length

class MapJudgeToPresentationScores(models.Model):
    judgeid = models.IntegerField()
    scoresheetid = models.IntegerField()

class MapJudgeToJournalScores(models.Model):
    judgeid = models.IntegerField()
    scoresheetid = models.IntegerField()

class MapJudgeToMachineDesignScores(models.Model):
    judgeid = models.IntegerField()
    scoresheetid = models.IntegerField()

class PresentationScores(models.Model):
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()
    field4 = models.IntegerField()
    field5 = models.IntegerField()
    field6 = models.IntegerField()
    field7 = models.IntegerField()
    field8 = models.IntegerField()
    penalty = models.IntegerField()

class JournalScores(models.Model):
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()
    field4 = models.IntegerField()
    field5 = models.IntegerField()
    field6 = models.IntegerField()
    field7 = models.IntegerField()
    field8 = models.IntegerField()

class MachineDesignScores(models.Model):
    field1 = models.IntegerField()
    field2 = models.IntegerField()
    field3 = models.IntegerField()
    field4 = models.IntegerField()
    field5 = models.IntegerField()
    field6 = models.IntegerField()
    field7 = models.IntegerField()
    field8 = models.IntegerField()

class Penalties(models.Model):
    PresentationPenalties = models.IntegerField()
    MachinePenalties = models.IntegerField()


class MapTeamToPresentationScores(models.Model):
    teamid = models.IntegerField()
    scoresheetid = models.IntegerField()

class MapTeamToJournalScores(models.Model):
    teamid = models.IntegerField()
    scoresheetid = models.IntegerField()

class MapTeamToMachineDesignScores(models.Model):
    teamid = models.IntegerField()
    scoresheetid = models.IntegerField()

class MapTeamToPenalties(models.Model):
    teamid = models.IntegerField()
    scoresheetid = models.IntegerField()
