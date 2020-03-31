import sys

# this.py '   1920x1080     60.00*+' 'center'
args = sys.argv[1:]
reso = args[0]

width, height = reso.split()[0].split('x')
width = int(width)
height = int(height)

cmd = args[1]

if (cmd == 'center'):
	w = 0.5 * width
	h = 0.7 * height
	x = (w - width) * 0.5
	y = (h - height) * 0.5
	wmctrl = 'wmctrl -r :ACTIVE: -e \'{}\''.format(
		','.join([
			str(int(abs(a))) for a in [0, x, y, w, h]
		])
	)
	print(
		' ; '.join([
			'wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz',
			wmctrl
		])
	)
elif (cmd == 'maximize'):
	print('wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz')
