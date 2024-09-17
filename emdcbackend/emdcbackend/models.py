from django.db import models

# this is where tables get made for the data.

class Judge(models.Model):
  jid = models.IntegerField(max_length=4, unique=True)
  uid = models.IntegerField(max_length=4)
  clusterid = models.IntegerField(max_length=4)

class JudgeClusters(models.Model):
  clusterid = models.IntegerField(max_length=4, unique=True)
  cid = models.IntegerField(max_length=4)

class Teams(models.Model):
  tid = models.IntegerField(max_length=4, unique=True)
  team_name = models.CharField(max_length=99)
  school_name = models.CharField(max_length=99)
  cid = models.IntegerField(max_length=4) # used as a secondary key for the contest
  journal_score = models.FloatField()
  presentation_score = models.FloatField()
  machinedesign_score = models.FloatField()
  score_penalties =models.FloatField()
  judge_cluster = models.IntegerField(max_length=4)


class Contest(models.Model):
  cid = models.IntegerField(max_length=4, unique=True)
  name = models.CharField(max_length=99)
  region = models.IntegerField(max_length=2)
  grade_level = models.IntegerField(max_length=1)
 