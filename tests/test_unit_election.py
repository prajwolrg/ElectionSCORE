from ..election import Election
from tbears.libs.scoretest.score_test_case import ScoreTestCase

class TestElection(ScoreTestCase):

	def setUp(self):
		super().setUp()
		self.score = self.get_score_instance(Election, self.test_account1)

	def test_hello(self):
		self.assertEqual(self.score.hello(), "Hello")

	def test_on_install(self):
		#Check if the SCORE owner is set as coordinator
		self.assertEqual(self.test_account1, self.score.owner)
		self.assertEqual(self.test_account1, self.score.coordinator_address())
		#Registration should be open by default
		self.assertEqual(self.score.is_registration_open(), True)
		#Voting should be closed by default
		self.assertEqual(self.score.is_voting_open(), False)

	# def test_registration(self):
	# 	self.set_tx(self.test_account2)
	# 	self.score.register_as_candidate()

	# 	print(self.score.get_candidates())