from address import bank_address

class bank:
	def __init__(self, idx, raw, fixed, addr):
		self.bank_id = idx
		self.raw = raw
		self.fixed = fixed
		self.addr = addr

	def seek(self, address):
		if self.bank_id != address.bank_id:
			raise 'wrong bank?'
		return self.seek_addr(address.addr)

	def tell(self):
		return self.raw.tell() + self.addr

	def seek_addr(self, addr):
		if addr < self.addr:
			raise Exception('bork %04X < %04X' % (addr, self.addr))
		old = self.tell()
		self.raw.seek(addr - self.addr)
		return old

	def includes(self, addr):
		return (addr >= self.addr) and (addr < self.addr + 0x4000)

def _init_mapper_000(a, c):
	raise 'boobs'

def _init_mapper_001(a, c):
	a.set_swap_area(0x8000, 0x4000)
	for i in range(0, len(c.prg) - 1):
		a.banks.append(bank(i, c.prg[i], False, 0x8000))
	idx = len(c.prg) - 1
	last = c.prg[idx]
	last.seek_end(0x06)
	a.banks.append(bank(idx, last, True, 0xC000))
	a.cbank = a.ibank = a.banks[-1]
	a.int_nmi = bank_address(a.ibank.bank_id, last.u16())
	a.int_rst = bank_address(a.ibank.bank_id, last.u16())
	a.int_irq = bank_address(a.ibank.bank_id, last.u16())
	# print('%04X, %04X, %04X' % (a.int_reset, a.int_nmi, a.int_irq))

_mappers = {
	0: _init_mapper_000,
	1: _init_mapper_001
}

def initialize_analyzer(a, c):
	if c.mapper not in _mappers:
		raise Exception('Mapper "%03X" not supported')
	_mappers[int(c.mapper)](a, c)



