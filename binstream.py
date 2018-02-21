import io

class binstream:
	def __init__(self, stream):
		self.st = stream
		self.st.seek(0, 2)
		self._size = self.st.tell()
		self.st.seek(0)

	def size(self):
		return self._size

	def u8(self):
		return ord(self.st.read(1)) & 0xff

	def u16(self):
		lo = self.u8()
		hi = self.u8() << 8
		return (lo | hi)

	def u32(self):
		v  = self.u8()
		v |= self.u8() << 8
		v |= self.u8() << 16
		v |= self.u8() << 24
		return v

	def uint(self, n):
		if 1 == n:
			return self.u8()
		elif 2 == n:
			return self.u16()
		elif 4 == n:
			return self.u32()
		return None

	def skip(self, n):
		self.st.seek(n, 1)

	def tell(self):
		return self.st.tell()

	def seek(self, off, org = 0):
		self.st.seek(off, org)

	def seek_end(self, off):
		self.st.seek(off * -1, 2)

	def rewind(self):
		self.st.seek(0)

	def substream(self, n):
		return binstream(io.BytesIO(self.st.read(n)))



