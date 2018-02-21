from binstream import binstream
from dotmap import DotMap

INES_MAGIC = 0x1A53454E

def _flags_6(b):
	v = b.u8()
	return DotMap({
		'vertical_mirror': bool(v & 1),
		'battery_backed': bool(v & 2),
		'has_trainer': bool(v & 4),
		'ignore_mirror': bool(v & 8),
		'lower_mapper': (v >> 4)
		})

def _flags_7(b):
	v = b.u8()
	return DotMap({
		'vs_unisystem': bool(v & 1),
		'playchoice_10': bool(v & 2),
		'ines2': bool(2 == ((v >> 2) & 0x03)),
		'upper_mapper': v >> 4
		})

def _flags_9(b):
	v = b.u8()
	return DotMap({
		'pal': bool(v & 1),
		'reserved': (v >> 1)
		})

def _try_load_as_ines(b):
	if INES_MAGIC != b.u32():
		# log
		return None
	nprg = b.u8()
	nchr = b.u8()
	f6 = _flags_6(b)
	f7 = _flags_7(b)
	if f7.ines2:
		# log
		return None
	prg_ram_size = 0x2000 * b.u8()
	if 0 == prg_ram_size:
		prg_ram_size = 0x2000
	f9 = _flags_9(b)
	# todo honor _flags_10()...
	b.skip(1 + 5)
	p = [ b.substream(0x4000) for i in range(0, nprg) ]
	c = [ b.substream(0x2000) for i in range(0, nchr) ]
	return DotMap({ 'prg': p, 'chr': c, 
		'mapper': f6.lower_mapper | (f7.upper_mapper << 8) })

def load(filename):
	b = binstream(open(filename, 'rb'))
	c = _try_load_as_ines(b)
	#
	# Try load as other formats...
	#
	return c


