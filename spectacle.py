import sys

# this.py '   1920x1080     60.00*+' 'center'
args = sys.argv[1:]
reso = args[0]

width, height = reso.split()[0].split('x')
width = int(width)
height = int(height)

cmd = args[1]

removeMaximized = 'wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz'
addMaximizedVert = 'wmctrl -r :ACTIVE: -b add,maximized_vert'

def commaSeparated(arr):
	return ','.join([
			str(int(abs(a))) for a in arr
		]
	)


if (cmd == 'center'):
	w = 0.5 * width
	h = 0.7 * height
	x = (w - width) * 0.5
	y = (h - height) * 0.5
	wmctrl = 'wmctrl -r :ACTIVE: -e \'{}\''.format(
		commaSeparated([0, x, y, w, h])
	)
	print(
		' ; '.join([
			removeMaximized,
			wmctrl
		])
	)
elif (cmd == 'maximize'):
	print('wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz')
elif (cmd == 'right'):
	w = 0.5 * width
	h = height
	x = width - w
	y = 0
	wmctrl = 'wmctrl -r :ACTIVE: -e \'{}\''.format(
		commaSeparated([0, x, y, w, h])
	)
	print(
		' ; '.join([
			removeMaximized,
			wmctrl,
			addMaximizedVert,
		])
	)
elif (cmd == 'left'):
	w = 0.5 * width
	h = height
	x = 0
	y = 0
	wmctrl = 'wmctrl -r :ACTIVE: -e \'{}\''.format(
		commaSeparated([0, x, y, w, h])
	)
	print(
		' ; '.join([
			removeMaximized,
			wmctrl,
			addMaximizedVert,
		])
	)
