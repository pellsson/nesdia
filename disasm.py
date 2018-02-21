from address import bank_address

OPR_NONE = 0
OPR_A = 1
OPR_IMM = 2
OPR_REL = 3
OPR_ZPG = 4
OPR_ZPG_X = 5
OPR_ZPG_Y = 6
OPR_IND_X = 7
OPR_IND_Y = 8
OPR_ABS = 9
OPR_ABS_Y = 10
OPR_ABS_X = 11
OPR_IND = 12

class opcode:
	def __init__(self, name, opr = OPR_NONE):
		self.name = name
		self.opr = opr

opc_undef = opcode('und', OPR_NONE)
decoder = [
	# 0x00
	opcode('brk'),				opcode('ora', OPR_IND_X),
	opc_undef,					opc_undef,
	opc_undef,					opcode('ora', OPR_ZPG),	
	opcode('asl', OPR_ZPG),		opcode('php'),
	opcode('ora', OPR_IMM),		opcode('asl', OPR_IMM),
	opcode('asl', OPR_A),		opc_undef,
	opc_undef,					opcode('ora', OPR_ABS),
	opcode('asl', OPR_ABS),		opc_undef,
	# 0x10
	opcode('bpl', OPR_REL),		opcode('ora', OPR_IND_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('ora', OPR_ZPG_X),
	opcode('asl', OPR_ZPG_X),	opc_undef,
	opcode('clc'),				opcode('ora', OPR_ABS_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('ora', OPR_ABS_X),
	opcode('asl', OPR_ABS_X),	opc_undef,
	# 0x20
	opcode('jsr', OPR_ABS),		opcode('and', OPR_IND_X),
	opc_undef,					opc_undef,
	opcode('bit', OPR_ZPG),		opcode('and', OPR_ZPG),
	opcode('rol', OPR_ZPG),		opc_undef,
	opcode('plp'),				opcode('and', OPR_IMM),
	opcode('rol', OPR_A),		opc_undef,
	opcode('bit', OPR_ABS),		opcode('and', OPR_ABS),
	opcode('rol', OPR_ABS),		opc_undef,
	# 0x30
	opcode('bmi', OPR_REL),		opcode('and', OPR_IND_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('and', OPR_ZPG_X),
	opcode('rol', OPR_ZPG_X),	opc_undef,
	opcode('sec'),				opcode('and', OPR_ABS_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('and', OPR_ABS_X),
	opcode('rol', OPR_ABS_X),	opc_undef,
	# 0x40
	opcode('rti'),				opcode('eor', OPR_IND_X),
	opc_undef,					opc_undef,
	opc_undef,					opcode('eor', OPR_ZPG),
	opcode('lsr', OPR_ZPG),		opc_undef,
	opcode('pha'),				opcode('eor', OPR_IMM),
	opcode('lsr', OPR_A),		opc_undef,
	opcode('jmp', OPR_ABS),		opcode('eor', OPR_ABS),
	opcode('lsr', OPR_ABS),		opc_undef,
	# 0x50
	opcode('bvc', OPR_REL),		opcode('eor', OPR_IND_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('eor', OPR_ZPG_X),
	opcode('lsr', OPR_ZPG_X),	opc_undef,
	opcode('cli'),				opcode('eor', OPR_ABS_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('eor', OPR_ABS_X),
	opcode('lsr', OPR_ABS_X),	opc_undef,
	# 0x60
	opcode('rts'),				opcode('adc', OPR_IND_X),
	opc_undef,					opc_undef,
	opc_undef,					opcode('adc', OPR_ZPG),
	opcode('ror', OPR_ZPG),		opc_undef,
	opcode('pla'),				opcode('adc', OPR_IMM),
	opcode('ror', OPR_A),		opc_undef,
	opcode('jmp', OPR_IND),		opcode('adc', OPR_ABS),
	opcode('ror', OPR_ABS),		opc_undef,
	# 0x70
	opcode('bvs', OPR_REL),		opcode('adc', OPR_IND_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('adc', OPR_ZPG_X),
	opcode('ror', OPR_ZPG_X),	opc_undef,
	opcode('sei'),				opcode('adc', OPR_ABS_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('adc', OPR_ABS_X),
	opcode('ror', OPR_ABS_X),	opc_undef,
	# 0x80
	opc_undef,					opcode('sta', OPR_IND_X),
	opc_undef, 					opc_undef,
	opcode('sty', OPR_ZPG),		opcode('sta', OPR_ZPG),
	opcode('stx', OPR_ZPG),		opc_undef,
	opcode('dey'),				opc_undef,
	opcode('txa'),				opc_undef,
	opcode('sty', OPR_ABS),		opcode('sta', OPR_ABS),
	opcode('stx', OPR_ABS),		opc_undef,
	# 0x90
	opcode('bcc', OPR_REL),		opcode('sta', OPR_IND_Y),
	opc_undef,					opc_undef,
	opcode('sty', OPR_ZPG_X),	opcode('sta', OPR_ZPG_X),
	opcode('stx', OPR_ZPG_Y),	opc_undef,
	opcode('tya'),				opcode('sta', OPR_ABS_Y),
	opcode('txs'),				opc_undef,
	opc_undef,					opcode('sta', OPR_ABS_X),
	opc_undef,					opc_undef,
	# 0xA0
	opcode('ldy', OPR_IMM),		opcode('lda', OPR_IND_X),
	opcode('ldx', OPR_IMM),		opc_undef,
	opcode('ldy', OPR_ZPG),		opcode('lda', OPR_ZPG),
	opcode('ldx', OPR_ZPG),		opc_undef,
	opcode('tay'),				opcode('lda', OPR_IMM),
	opcode('tax'),				opc_undef,
	opcode('ldy', OPR_ABS),		opcode('lda', OPR_ABS),
	opcode('ldx', OPR_ABS),		opc_undef,
	# 0xB0
	opcode('bcs', OPR_REL), 	opcode('lda', OPR_IND_Y),
	opc_undef,					opc_undef,
	opcode('ldy', OPR_ZPG_X),	opcode('lda', OPR_ZPG_X),
	opcode('ldx', OPR_ZPG_Y),	opc_undef,
	opcode('clv'),				opcode('lda', OPR_ABS_Y),
	opcode('tsx'),				opc_undef,
	opcode('ldy', OPR_ABS_X),	opcode('lda', OPR_ABS_X),
	opcode('ldx', OPR_ABS_Y),	opc_undef,
	# 0xC0
	opcode('cpy', OPR_IMM),		opcode('cmp', OPR_IND_X),
	opc_undef,					opc_undef,
	opcode('cpy', OPR_ZPG),		opcode('cmp', OPR_ZPG),
	opcode('dec', OPR_ZPG),		opc_undef,
	opcode('iny'),				opcode('cmp', OPR_IMM),
	opcode('dex'),				opc_undef,
	opcode('cpy', OPR_ABS),		opcode('cmp', OPR_ABS),
	opcode('dec', OPR_ABS),		opc_undef,
	# 0xD0
	opcode('bne', OPR_REL),		opcode('cmp', OPR_IND_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('cmp', OPR_ZPG_X),
	opcode('dec', OPR_ZPG_X),	opc_undef,
	opcode('cld'),				opcode('cmp', OPR_ABS_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('cmp', OPR_ABS_X),
	opcode('dec', OPR_ABS_X),	opc_undef,
	# 0xE0
	opcode('cpx', OPR_IMM),		opcode('sbc', OPR_IND_X),
	opc_undef,					opc_undef,
	opcode('cpx', OPR_ZPG),		opcode('sbc', OPR_ZPG),
	opcode('inc', OPR_ZPG),		opc_undef,
	opcode('inx'),				opcode('sbc', OPR_IMM),
	opcode('nop'),				opc_undef,
	opcode('cpx', OPR_ABS),		opcode('sbc', OPR_ABS),
	opcode('inc', OPR_ABS),		opc_undef,
	# 0xF0
	opcode('beq', OPR_REL),		opcode('sbc', OPR_IND_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('sbc', OPR_ZPG_X),
	opcode('inc', OPR_ZPG_X),	opc_undef,
	opcode('sed'),				opcode('sbc', OPR_ABS_Y),
	opc_undef,					opc_undef,
	opc_undef,					opcode('sbc', OPR_ABS_X),
	opcode('inc', OPR_ABS_X),	opc_undef
]

class instruction(bank_address):
	def __init__(self, address, mnem, opr, size, val):
		super().__init__(address.bank_id, address.addr)
		self.mnem = mnem
		self.opr = opr
		self.size = size
		self.val = val
		self.branch_to = None
		self.conditional = False
	def is_imm(self):
		return OPR_IMM == self.opr

jumps = [ 'jsr', 'jmp' ]

def one(pc, b):
	x = decoder[b.u8()]
	size = 0
	if x.opr >= OPR_IMM:
		size += 1
		if x.opr >= OPR_ABS:
			size += 1

	inst = instruction(pc, x.name, x.opr, 1 + size, b.uint(size))

	if OPR_REL == inst.opr:
		inst.conditional = True
		if inst.val & 0x80:
			inst.branch_to = (pc.addr + 2) - ((inst.val ^ 0xff) + 1)
		else:
			inst.branch_to = (pc.addr + 2) + inst.val
	elif OPR_IND != inst.opr and inst.mnem in jumps:
		inst.branch_to = inst.val

	return inst
