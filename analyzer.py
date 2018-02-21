import disasm
import bisect
import mapper
from dotmap import DotMap
from address import bank_address
from symbols import *

NOT_PRG_BANK = 0x8000 #hack...

end_of_function = [ 'und', 'rti', 'rts', 'jmp' ]

class analyzer:
	def __init__(self):
		self.banks = []
		self.symbols = []
		self.sym_ref_list = []

	def set_swap_area(self, start, size):
		self.swap_start = start
		self.swap_size = size

	def find_symbol(self, address):
		idx = bank_address.find_exact_in(self.symbols, address)
		if not idx:
			return None
		return self.symbols[idx]

	def next_symbol(self, address):
		idx = bisect.bisect_right(self.symbols, address)
		if idx == len(self.symbols):
			return None
		while idx < len(self.symbols):
			if self.symbols[idx].composite != address.composite:
				break
			else:
				idx += 1
		if idx == len(self.symbols):
			return None
		return self.symbols[idx]

	def _create_symbol(self, sym_type, address, **kwarg):
		# todo: kill me?
		sym = self.find_symbol(address)
		if sym:
			if not isinstance(sym, sym_type):
				raise Exception('Symbol type %d != %d - cant redefine atm...' % (sym.type_id, t))
		else:
			sym = sym_type(address)
			bisect.insort_left(self.symbols, sym)
			self.sym_ref_list.append(sym)
			sym.ref_index = len(self.sym_ref_list) - 1

		if 'name' in kwarg:
			sym._name = kwarg['name']
		if 'size' in kwarg:
			sym.size = kwarg['size']
		if 'comment' in kwarg:
			sym.comment = kwarg['comment']
		if 'ref_by' in kwarg:
			sym.add_refed_by(kwarg['ref_by'])
		return sym

	def create_data_sym(self, address, **kwarg):
		return self._create_symbol(data_symbol, address, **kwarg)
	def create_func_sym(self, address, **kwarg):
		sym = self._create_symbol(func_symbol, address, **kwarg)
		return sym
	def create_label_sym(self, address, **kwarg):
		sym = self.find_symbol(address)
		if sym and isinstance(sym, func_symbol):
			sym.add_refed_by(kwarg['ref_by'])
			return sym
		return self._create_symbol(label_symbol, address, **kwarg)
	def create_unknown_sym(self, address, **kwarg):
		return self._create_symbol(unknown_symbol, address, **kwarg)

	def is_bank_accessible(self, bank_id):
		if (self.cbank.bank_id == bank_id) or (bank_id & NOT_PRG_BANK):
			return True
		return self.banks[bank_id].fixed

	def is_address_accessible(self, address):
		return self.is_bank_accessible(address.bank_id)

	def _find_max_sym_addr(self, address):
		b = self.cbank
		if not self.is_address_accessible(address):
			raise Exception('solve this')
		nextsym = self.next_symbol(address)
		if None == nextsym or not self.is_address_accessible(nextsym):
			return (b.addr + 0x4000)
		return nextsym.addr

	def is_func_end(self, mnem, pc, cond):
		if mnem not in end_of_function:
			return False
		for it in cond:
			if it.dst.equal(pc):
				print('Found end, but its branched...')
				return False
		return True

	def is_inside_swap(self, addr):
		s = self.swap_start
		e = self.swap_start + self.swap_size
		return (addr >= s) and (addr < e)

	def analyze_function(self, address, ref_by, name = None):
		old = self.find_symbol(address)
		if old:
			print('Function "%s" already analyzed' % (old.get_name()))
			old.add_refed_by(ref_by)
			return old

		sym = self.create_func_sym(address, name = name, ref_by = ref_by)
		max_addr = self._find_max_sym_addr(address)
		b = self.cbank

		print('Analyzing function @ %s' % (address))
		old_off = b.seek(address)
		pc = bank_address(b.bank_id, address.addr)
		cond = []
		while pc.addr < max_addr - 1:
			inst = disasm.one(pc, b.raw)
			if inst.branch_to:
				# print('%s: %s $%04X (%d bytes)' % (str(pc), inst.mnem, inst.branch_to, inst.size))
				if not self.is_inside_swap(inst.branch_to) or b.includes(inst.branch_to):
					dst = bank_address(b.bank_id, inst.branch_to)
					if inst.conditional:
						cond.append(DotMap({ 'src': inst, 'dst': dst }))
					else:
						n = self.analyze_function(dst, inst)
				else:
					print('Branch to different bank ## TODO')
			pc.add(inst.size)
			sym.instructions.append(inst)
			if self.is_func_end(inst.mnem, pc, cond):
				print('Function end: %s' % (inst.mnem))
				break
		if pc.addr > max_addr:
			# split instruction.
			raise Exception('solve meeeh')

		sym.size = pc.addr - address.addr
		end = address.addr + sym.size

		for it in cond:
			if it.dst < address or it.dst.addr > end:
				n = self.analyze_function(it.dst, it.src)
			elif pc.addr >= max_addr and it.dst.addr == end:
				raise Exception('Function should have been extended!')
			else:
				self.create_label_sym(it.dst, ref_by=it.src)

		b.seek_addr(old_off)
		return sym

	def associate_labels(self):
		n = len(self.symbols)
		idx = 0
		while idx < n:
			sub = self.symbols[idx]
			if isinstance(sub, label_symbol):
				raise Exception('what the hell?')
			elif not isinstance(sub, func_symbol):
				continue
			for i in range(idx + 1, n):
				lbl = self.symbols[i]
				if isinstance(lbl, label_symbol):
					sub.add_label(lbl)
				elif isinstance(lbl, func_symbol):
					break
				idx += 1 # skip it...
			idx += 1

	def insert_unknowns(self):
		pass

	def run_analysis(self):
		#
		# Add interrupt vector table as symbols
		#
		nmi_sym = self.create_data_sym(
			bank_address(self.ibank.bank_id, 0xfffa),
			name = 'nmi_vector_offset', size = 2, comment = 'Interrupt vector table')
		rst_sym = self.create_data_sym(
			bank_address(self.ibank.bank_id, 0xfffc),
			name = 'rst_vector_offset', size = 2)
		irq_sym = self.create_data_sym(
			bank_address(self.ibank.bank_id, 0xfffe),
			name = 'irq_vector_offset', size = 2)
		#
		# Run analysis from each interrupt vector
		#
		self.analyze_function(self.int_nmi, nmi_sym, 'on_nmi')
		self.analyze_function(self.int_rst, rst_sym, 'on_rst')
		self.analyze_function(self.int_irq, irq_sym, 'on_irq')
		#
		# Analysis done. Do finishing touches :)
		#
		self.associate_labels()
		self.insert_unknowns()

def create(c):
	a = analyzer()
	mapper.initialize_analyzer(a, c)
	a.run_analysis()
	return a
