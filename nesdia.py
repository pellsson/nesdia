import cart
import sys
import analyzer
import view
import window

if len(sys.argv) < 2:
	print('You need to specify a file to analyze...')
	sys.exit(-1)

c = cart.load(sys.argv[1])
if not c:
	print('Failed to load the nes file. Probably not supported.')
	sys.exit(-1)

a = analyzer.create(c)
view.create(a, 'x816')

# window.run()