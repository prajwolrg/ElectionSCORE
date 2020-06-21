from iconservice import *

TAG = 'Election'

class Election(IconScoreBase):

	_ADDR_COORDINATOR = 'addr_coordinator'
	_REGISTRATION_OPEN = 'registration_open'
   # _REGISTRATION_DEADLINE = 'registration_deadline'
   # _VOTING_DEADLINE = 'voting_deadline'
	_PENDING_CANDIDATES = 'pending_candidates'
	_PENDING_VOTERS = 'pending_voters'
	_REGISTERED_CANDIDATES = 'registered_candidates'
	_REGISTERED_VOTERS = 'registered_voters'
	_VOTING_OPEN = 'voting_open'

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)
		self._addr_coordinator = VarDB(Election._ADDR_COORDINATOR, db, Address)
		self._registration_open = VarDB(Election._REGISTRATION_OPEN, db, bool)
		#self._registration_deadline = VarDB(Election._REGISTRATION_DEADLINE, db, int)
		#self._voting_deadline = VarDB(Election._VOTING_DEADLINE, db, int)
		self._pending_candidates = ArrayDB(Election._PENDING_CANDIDATES, db, bool)
		self._pending_voters = ArrayDB(Election._PENDING_VOTERS, db, str)
		self._registered_candidates = ArrayDB(Election._REGISTERED_CANDIDATES, db, str)
		self._registered_voters = ArrayDB(Election._REGISTERED_VOTERS, db, str)
		self._voting_open = VarDB(Election._VOTING_OPEN, db, bool)

	def on_install(self) -> None:
		super().on_install()
		self._addr_coordinator.set(self.msg.sender)
		self._registration_open.set(True)
		self._voting_open.set(False)

	def on_update(self) -> None:
		super().on_update()

	@external(readonly=True)
	def hello(self) -> str:
		Logger.debug(f'Hello, world!', TAG)
		return "Hello"

	def only_owner(func):
		@wraps(func)
		def __wrapper(self:object, *args, **kwargs):
			if self.msg.sender != self.owner:
				revert(f'You do not have this previlege')
			return func(self, *args, **kwargs)
		return __wrapper

	@external
	def register_as_candidate(self) -> None:
		if self._registration_open.get():
			self._pending_candidates.put(self.msg.sender)
		else:
			revert('The registration is already closed.')

	@external(readonly=True)
	def get_candidates(self) -> list:
		candidates = []
		for candidate in self._registered_candidates:
			candidates.append(candidate)

		return candidates

	@external(readonly=True)
	def is_voting_open(self) ->bool:
		return self._voting_open.get()

	@external(readonly=True)
	def is_registration_open(self) -> bool:
		return self._registration_open.get()

	@external(readonly=True)
	def coordinator_address(self) -> str:
		return self._addr_coordinator.get()

	@external
	# @only_owner
	def approve_candidates(self, candidate:Address) -> None:
		if candidate in self._pending_candidates & self._registration_open.get():
			if candidate in self._registered_candidates:
				revert(f'{candidate} is already registered.')
			else:
				self._registered_voters.put(candidate)
		else:
			revert(f'{candidate} has not registered yet.')

	@external
	# @only_owner
	def approve_voters(self, voter:Address) -> None:
		if voter in self._pending_candidates & self._registration_open.get():
			if voter in self._registered_voters:
				revert(f'{voter} is already registered.')
			else:
				self._registered_voters.put(candidate)
		else:
			revert(f'{voter} has not registered yet.')

	# @external
	# @only_owner
	# def close_registration(self) -> None:
	#	 if (self._registration_open.get()):
	#		 self._registration_open.set(False)
	#	 else:
	#		 revert(f'The registration is already closed.')

	@external
	# @only_owner
	def toggle_registration(self) -> None:
		self._registration_open.set(not self._registration_open.get())

	@external
	# @only_owner
	def close_voting(self) -> None:
		if (self._voting_open.get()):
			self._voting_open.set(False)
		else:
			revert(f'The voting is already closed.')