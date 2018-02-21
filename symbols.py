from address import bank_address

class symbol(bank_address):
	def __init__(self, address):
		super().__init__(address.bank_id, address.addr)
		self._name = None
		self.comment = ''
		self.size = 1
	def get_name(self):
		if not self._name:
			return self._default_name()
		return self._name

	def __repr__(self):
		return 'address=%s, name=%s, size=%d' % (super().__repr__(), self.name, self.size)

class data_symbol(symbol):
	def __init__(self, address):
		super().__init__(address)
	def __repr__(self):
		return 'data_symbol(%s)' % (super().__repr__())
	def _default_name(self):
		return 'data_%d_%04X' % (self.bank_id, self.addr)

class func_symbol(symbol):
	def __init__(self, address):
		super().__init__(address)
		self.instructions = []
		self.labels = []
	def add_instruction(self, inst):
		self.instructions.append(inst)
	def add_label(self, lbl):
		self.labels.append(lbl)
		lbl.function = self
	def _default_name(self):
		return 'subroutine_%d_%04X' % (self.bank_id, self.addr)
	def __repr__(self):
		return 'func_symbol(%s)' % (super().__repr__())

class label_symbol(symbol):
	def __init__(self, address):
		super().__init__(address)
		self.function = None
	def __repr__(self):
		return 'label_symbol(%s)' % (super().__repr__())
	def _default_name(self):
		return 'loc_%d_%04X' % (self.bank_id, self.addr)

class unknown_symbol(symbol):
	def __init__(self, address):
		super().__init__(address)
	def _default_name(self):
		return 'unknown_%d_%04X' % (self.bank_id, self.addr)
	def __repr__(self):
		return 'unknown_symbol(%s)' % (super().__repr__())

