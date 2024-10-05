from django.test import TestCase
from ..models import (
    Contest,
    MapContestToJudge,
    MapContestToTeam,
    MapContestToOrganizer,
    Judge,
    MapJudgeToCluster,
    JudgeClusters,
    MapClusterToTeam,
    Teams,
    MapUserToRole,
    Coach,
    Admin,
    MapCoachToTeam,
    Organizer,
    MapJudgeToPresentationScores,
    MapJudgeToJournalScores,
    MapJudgeToMachineDesignScores,
    Scoresheet,
    Penalties,
    MapTeamToPresentationScores,
    MapTeamToJournalScores,
    MapTeamToMachineDesignScores,
    MapTeamToPenalties,
)

class ContestModelTest(TestCase):
    def test_contest_creation(self):
        contest = Contest.objects.create(name="Math Contest", is_open=True, is_tabulated=False)
        self.assertEqual(contest.name, "Math Contest")
        self.assertTrue(contest.is_open)
        self.assertFalse(contest.is_tabulated)

class MapContestToJudgeModelTest(TestCase):
    def test_map_contest_to_judge_creation(self):
        mapping = MapContestToJudge.objects.create(contestid=1, judgeid=2)
        self.assertEqual(mapping.contestid, 1)
        self.assertEqual(mapping.judgeid, 2)

class MapContestToTeamModelTest(TestCase):
    def test_map_contest_to_team_creation(self):
        mapping = MapContestToTeam.objects.create(contestid=1, teamid=3)
        self.assertEqual(mapping.contestid, 1)
        self.assertEqual(mapping.teamid, 3)

class MapContestToOrganizerModelTest(TestCase):
    def test_map_contest_to_organizer_creation(self):
        mapping = MapContestToOrganizer.objects.create(contestid=1, organizerid=4)
        self.assertEqual(mapping.contestid, 1)
        self.assertEqual(mapping.organizerid, 4)

class JudgeModelTest(TestCase):
    def test_judge_creation(self):
        judge = Judge.objects.create(first_name="Alice", last_name="Brown", contestid=1, presentation=True, mdo=False, journal=True, penalties=False)
        self.assertEqual(judge.first_name, "Alice")
        self.assertEqual(judge.last_name, "Brown")
        self.assertEqual(judge.contestid, 1)
        self.assertTrue(judge.presentation)

class MapJudgeToClusterModelTest(TestCase):
    def test_map_judge_to_cluster_creation(self):
        mapping = MapJudgeToCluster.objects.create(judegeid=5, clusterid=1)
        self.assertEqual(mapping.judegeid, 5)
        self.assertEqual(mapping.clusterid, 1)

class JudgeClustersModelTest(TestCase):
    def test_judge_cluster_creation(self):
        cluster = JudgeClusters.objects.create(cluster_name="Cluster A")
        self.assertEqual(cluster.cluster_name, "Cluster A")

class MapClusterToTeamModelTest(TestCase):
    def test_map_cluster_to_team_creation(self):
        mapping = MapClusterToTeam.objects.create(clusterid=1, teamid=2)
        self.assertEqual(mapping.clusterid, 1)
        self.assertEqual(mapping.teamid, 2)

class TeamsModelTest(TestCase):
    def test_team_creation(self):
        team = Teams.objects.create(
            team_name="Team Alpha",
            journal_score=95.0,
            presentation_score=90.0,
            machinedesign_score=85.0,
            score_penalties=0.0,
            judge_cluster=1
        )
        self.assertEqual(team.team_name, "Team Alpha")
        self.assertEqual(team.journal_score, 95.0)

class MapUserToRoleModelTest(TestCase):
    def test_map_user_to_role_creation(self):
        mapping = MapUserToRole.objects.create(role=1, uuid=1, relatedid=2)
        self.assertEqual(mapping.role, 1)
        self.assertEqual(mapping.uuid, 1)

class CoachModelTest(TestCase):
    def test_coach_creation(self):
        coach = Coach.objects.create(first_name="John", last_name="Doe", school_name="High School")
        self.assertEqual(coach.first_name, "John")

class AdminModelTest(TestCase):
    def test_admin_creation(self):
        admin = Admin.objects.create(first_name="Sara", last_name="Connor")
        self.assertEqual(admin.first_name, "Sara")

class MapCoachToTeamModelTest(TestCase):
    def test_map_coach_to_team_creation(self):
        mapping = MapCoachToTeam.objects.create(teamid=1, coachid=2)
        self.assertEqual(mapping.teamid, 1)

class OrganizerModelTest(TestCase):
    def test_organizer_creation(self):
        organizer = Organizer.objects.create(first_name="Alice", last_name="Johnson", region="South")
        self.assertEqual(organizer.first_name, "Alice")

class MapJudgeToPresentationScoresModelTest(TestCase):
    def test_map_judge_to_presentation_scores_creation(self):
        mapping = MapJudgeToPresentationScores.objects.create(judgeid=1, scoresheetid=1)
        self.assertEqual(mapping.judgeid, 1)

class MapJudgeToJournalScoresModelTest(TestCase):
    def test_map_judge_to_journal_scores_creation(self):
        mapping = MapJudgeToJournalScores.objects.create(judgeid=1, scoresheetid=2)
        self.assertEqual(mapping.judgeid, 1)

class MapJudgeToMachineDesignScoresModelTest(TestCase):
    def test_map_judge_to_machine_design_scores_creation(self):
        mapping = MapJudgeToMachineDesignScores.objects.create(judgeid=1, scoresheetid=3)
        self.assertEqual(mapping.judgeid, 1)

class ScoresheetModelTest(TestCase):
    def test_scoresheet_creation(self):
        scoresheet = Scoresheet.objects.create(
            sheetType=Scoresheet.ScoresheetEnum.PRESENTATION,
            field1=1,
            field2=2,
            field3=3,
            field4=4,
            field5=5,
            field6=6,
            field7=7,
            field8=8,
        )
        self.assertEqual(scoresheet.sheetType, Scoresheet.ScoresheetEnum.PRESENTATION)

class PenaltiesModelTest(TestCase):
    def test_penalties_creation(self):
        penalties = Penalties.objects.create(PresentationPenalties=1, MachinePenalties=2)
        self.assertEqual(penalties.PresentationPenalties, 1)

class MapTeamToPresentationScoresModelTest(TestCase):
    def test_map_team_to_presentation_scores_creation(self):
        mapping = MapTeamToPresentationScores.objects.create(teamid=1, scoresheetid=1)
        self.assertEqual(mapping.teamid, 1)

class MapTeamToJournalScoresModelTest(TestCase):
    def test_map_team_to_journal_scores_creation(self):
        mapping = MapTeamToJournalScores.objects.create(teamid=1, scoresheetid=2)
        self.assertEqual(mapping.teamid, 1)

class MapTeamToMachineDesignScoresModelTest(TestCase):
    def test_map_team_to_machine_design_scores_creation(self):
        mapping = MapTeamToMachineDesignScores.objects.create(teamid=1, scoresheetid=3)
        self.assertEqual(mapping.teamid, 1)

class MapTeamToPenaltiesModelTest(TestCase):
    def test_map_team_to_penalties_creation(self):
        mapping = MapTeamToPenalties.objects.create(teamid=1, scoresheetid=4)
        self.assertEqual(mapping.teamid, 1)
