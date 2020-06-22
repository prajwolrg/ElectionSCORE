import os
import json

from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.libs.in_memory_zip import gen_deploy_data_content
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction

from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
from .utils import *

DIR_PATH = os.path.abspath(os.path.dirname(__file__))


class TestElection(IconIntegrateTestBase):
	TEST_HTTP_ENDPOINT_URI_V3 = "http://127.0.0.1:9000/api/v3"
	SCORE_PROJECT = os.path.abspath(os.path.join(DIR_PATH, '..'))

	def setUp(self):
		super().setUp()

		self.icon_service = None
		# if you want to send request to network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3
		# self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))

		# install SCORE
		self._operator = self._test1
		self._score_address = self._deploy_score(self.SCORE_PROJECT)['scoreAddress']
		self._user = self._wallet_array[0]
		self._attacker = self._wallet_array[1]

		for wallet in self._wallet_array:
			icx_transfer_call(super(), self._test1, wallet.get_address(), 100 * 10**18, self.icon_service)

		self._operator_icx_balance = get_icx_balance(super(), address=self._operator.get_address(), icon_service=self.icon_service)
		self._user_icx_balance = get_icx_balance(super(), address=self._user.get_address(), icon_service=self.icon_service)


	def _deploy_score(self, project, to: str = SCORE_INSTALL_ADDRESS) -> dict:
		# Generates an instance of transaction for deploying SCORE.
		transaction = DeployTransactionBuilder()\
			.from_(self._test1.get_address())\
			.to(to).step_limit(100_000_000_000)\
			.nid(3)\
			.nonce(100)\
			.content_type("application/zip")\
			.content(gen_deploy_data_content(project))\
			.build()

		# Returns the signed transaction object having a signature
		signed_transaction = SignedTransaction(transaction, self._test1)

		# process the transaction in local
		tx_result = self.process_transaction(signed_transaction, self.icon_service)

		self.assertEqual(True, tx_result['status'])
		self.assertTrue('scoreAddress' in tx_result)

		return tx_result

	
	def test_registration_open(self):
		is_registration_open = icx_call(
			super(),
			from_ = self._operator.get_address(),
			to_ = self._score_address,
			method = 'is_registration_open',
			icon_service = self.icon_service
		)
		self.assertTrue(is_registration_open == '0x1')

	def test_candidate_registration(self):
		length = icx_call(
			super(),
			from_ = self._wallet_array[0].get_address(),
			to_ = self._score_address,
			method = 'get_pending_registration_number',
			icon_service=self.icon_service
		)
		self.assertTrue(int(length, 16) == 0)
		
		result = transaction_call_success(
			super(),
			from_ = self._wallet_array[0],
			to_ = self._score_address,
			method = 'register_as_candidate',
			icon_service= self.icon_service
		)

		length = icx_call(
			super(),
			from_ = self._wallet_array[0].get_address(),
			to_ = self._score_address,
			method = 'get_pending_registration_number',
			icon_service=self.icon_service
		)
		self.assertTrue(int(length, 16) == 1)



""" 	def test_score_update(self):
		# update SCORE
		tx_result = self._deploy_score(self._score_address)

		self.assertEqual(self._score_address, tx_result['scoreAddress'])

	def test_initial_conditions(self):
		is_voting_open_call = CallBuilder().from_(self._test1.get_address()).to(self._score_address).method("is_voting_open").build() 
		is_voting_open_response = self.process_call(is_voting_open_call, self.icon_service)
		self.assertEqual('0x0', is_voting_open_response)

		is_registration_open_call = CallBuilder().from_(self._test1.get_address()).to(self._score_address).method("is_registration_open").build() 
		is_registration_open_response = self.process_call(is_registration_open_call, self.icon_service)
		self.assertEqual('0x1', is_registration_open_response) """

""" 	def test_registration(self):

		get_candidates_call = CallBuilder().from_(self._wallet_array[0].get_address()).to(self._score_address).method("get_candidates").build()
		get_candidate_response = self.process_call(get_candidates_call, self.icon_service)
		print(get_candidate_response)

		call_transaction = CallTransactionBuilder()\
			.from_(self._wallet_array[0].get_address()\
			.to(self._score_address) \
			.nid(3) \
			.nonce(100) \
			.method("register_as_candidate")\
			.build()

		estimate_step = self.icon_service.__class__
		(call_transaction)
		step_limit = estimate_step + 100000
		signed_transaction = self.SignedTransaction(call_transaction, wallet, step_limit)
		tx_hash = icon_service.send_transaction(signed_transaction)

 """