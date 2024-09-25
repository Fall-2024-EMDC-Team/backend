from django.db import models

# this is where tables get made for the data.

class Contest(models.Model):
  id = models.IntegerField(unique=True)
  name = models.CharField(max_length=99)
  is_open = models.BooleanField()
  is_tabulated = models.BooleanField()

class MapContestToJudge(models.Model):
  id = models.IntegerField(unique=True)
  contestid = models.IntegerField()
  judegeid = models.IntegerField()

class MapContestToTeam(models.Model):
  id = models.IntegerField(unique=True)
  contestid = models.IntegerField()
  teamid = models.IntegerField()

class MapContestToOrganizer(models.Model):
  id = models.IntegerField(unique=True)
  contestid = models.IntegerField()
  organizerid = models.IntegerField()

class MapContestToRegion(models.Model):
  id = models.IntegerField(unique=True)
  contestid = models.IntegerField()
  regionid = models.IntegerField()

class Region(models.Model):
  id = models.IntegerField(unique=True)
  name = models.CharField(max_length=99)

class Judge(models.Model):
  id = models.IntegerField(unique=True)
  first_name = models.CharField()
  last_name = models.CharField()
  contestid = models.IntegerField()

class MapJudgeToCluster(models.Model):
  id = models.IntegerField(unique=True)
  judegeid = models.IntegerField()
  clusterid = models.IntegerField()

class JudgeClusters(models.Model):
  id = models.IntegerField(unique=True)
  cluster_name = models.CharField()

class MapClusterToTeam(models.Model):
  id = models.IntegerField(unique=True)
  clusterid = models.IntegerField()
  teamid = models.IntegerField()

class Teams(models.Model):
  id = models.IntegerField(unique=True)
  team_name = models.CharField(max_length=99)
  school_name = models.CharField(max_length=99)
  journal_score = models.FloatField()
  presentation_score = models.FloatField()
  machinedesign_score = models.FloatField()
  score_penalties =models.FloatField()
  judge_cluster = models.IntegerField()

class MapUserToRole(models.Model):
  class RoleEnum(models.IntegerChoices):
        ADMIN = 1
        ORGANIZER = 2
        JUDGE = 3
        COACH = 4
  
  id = models.IntegerField(unique=True)
  role = models.IntegerField(choices=RoleEnum)
  uuid = models.IntegerField()
  relatedid = models.IntegerField()

class Coach(models.Model):
  id = models.IntegerField(unique=True)
  first_name = models.CharField()
  last_name = models.CharField()
  school_name = models.CharField()

class MapCoachToTeam(models.Model):
  id = models.IntegerField(unique=true)
  teamid = models.IntegerField()
  uuid = models.IntegerField()

class Organizer(models.Model):
  id = models.IntegerField(unique=True)
  first_name = models.CharField()
  last_name = models.CharField()

class MapJudgeToPresentationScores(models.Model):
  id = models.IntegerField(unique=True)
  judgeid = models.IntegerField()
  scoresheetid = models.IntegerField()

class MapJudgeToJournalScores(models.Model):
  id = models.IntegerField(unique=True)
  judgeid = models.IntegerField()
  scoresheetid = models.IntegerField()

class MapJudgeToMachineDesignScores(models.Model):
  id = models.IntegerField(unique=True)
  judgeid = models.IntegerField()
  scoresheetid = models.IntegerField()

class PresentationScores(models.Model):
  id = models.IntegerField(unique=True)
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
  id = models.IntegerField(unique=True)
  field1 = models.IntegerField()
  field2 = models.IntegerField()
  field3 = models.IntegerField()
  field4 = models.IntegerField()
  field5 = models.IntegerField()
  field6 = models.IntegerField()
  field7 = models.IntegerField()
  field8 = models.IntegerField()

class MachineDesignScores(models.Model):
  id = models.IntegerField(unique=True)
  field1 = models.IntegerField()
  field2 = models.IntegerField()
  field3 = models.IntegerField()
  field4 = models.IntegerField()
  field5 = models.IntegerField()
  field6 = models.IntegerField()
  field7 = models.IntegerField()
  field8 = models.IntegerField()

class MapTeamToPresentationScores(models.Model):
  id = models.IntegerField(unique=True)
  teamid = models.IntegerField()
  scoresheetid = models.IntegerField()

class MapTeamToJournalScores(models.Model):
  id = models.IntegerField(unique=True)
  teamid = models.IntegerField()
  scoresheetid = models.IntegerField()

class MapTeamToMachineDesignScores(models.Model):
  id = models.IntegerField(unique=True)
  teamid = models.IntegerField()
  scoresheetid = models.IntegerField()