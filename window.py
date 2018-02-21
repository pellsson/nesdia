import curses

class window:
	def __init__(self, x, y, w, h):
		self.win = curses.newwin(h, w, x, y)
		self.set_title('Disassembly')

	def _draw_text(self, x, y, str, c = None):
		self.win.addstr(y, x, str)
		self.invalid = True

	def set_title(self, title, c = None):
		self.win.box()
		self._draw_text(1, 0, title, c)

	def draw_text_at(self, x, y, str, c = None):
		self._draw_text(x + 1, x + y, str, c)

	def draw(self, force = False):
		if self.invalid or force:
			self.win.refresh()
		self.invalid = False

def _run(stdscr):
	stdscr.clear()
	stdscr.refresh()
	h, w = stdscr.getmaxyx()

	
	win = window(0, 0, w, int(h / 2))
	win.draw()

	# stdscr.addstr(0, 0, str(w))
	stdscr.getkey()

def run():
	curses.wrapper(_run)
	print('wat?')
