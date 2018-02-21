def create(a, fmt):

	for it in a.symbols:
		#print(it)
		if it.comment:
			print(';\n; %s\n;' % (it.comment))
		print('%02X:%04X    %s:' % (it.bank_id, it.addr, it.get_name()))
