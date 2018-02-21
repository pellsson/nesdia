import bisect

class bank_address:
	def __init__(self, bank_id, addr):
		self.bank_id = bank_id
		self.addr = addr
		self._update_composite()
		self.refed_by = []
		self.refs_to = []

	def add_refed_by(self, sym_or_address):
		if not bank_address.find_exact_in(self.refed_by, sym_or_address):
			bisect.insort_left(self.refed_by, sym_or_address)
		sym_or_address._add_ref_to(self)

	def _add_ref_to(self, sym_or_address):
		if not bank_address.find_exact_in(self.refs_to, sym_or_address):
			bisect.insort_left(self.refs_to, sym_or_address)

	def _update_composite(self):
		self.composite = (self.bank_id << 16) | self.addr

	def add(self, by):
		self.addr += by
		# todo honor bank boundaries
		self._update_composite()

	def equal(self, other):
		if not other:
			return False
		return self.composite == other.composite

	def __lt__(self, other):
		return self.composite < other.composite
	def __repr__(self):
		return '%02X:%04X' % (self.bank_id, self.addr)

	@staticmethod
	def find_exact_in(arr, address):
		idx = bisect.bisect_left(arr, address)
		if idx == len(arr):
			return None
		if arr[idx].composite != address.composite:
			return None
		return idx

