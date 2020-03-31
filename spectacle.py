import sys


removeMaximized = 'wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz'
addMaximized = 'wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz'
addMaximizedVert = 'wmctrl -r :ACTIVE: -b add,maximized_vert'

params = {
	'maximize': [None],
	'center': [0.7, 1.0],
	'left': [0.33, 0.5, 0.75],
	'right': [0.33, 0.5, 0.75],
}



def commaSeparated(arr):
	return ','.join([
			str(int(abs(a))) for a in arr
		]
	)



def makeResizeCmd(dims):
	return 'wmctrl -r :ACTIVE: -e \'{}\''.format(
		commaSeparated(dims)
	)



def printCombined(cmds):
	print(' ; '.join(cmds))



# this.py '   1920x1080     60.00*+' 'center'
args = sys.argv[1:]
reso = args[0]

width, height = reso.split()[0].split('x')
width = int(width)
height = int(height)

cmd = args[1]
filePath = '/tmp/spectacle-{}.txt'.format(cmd)
optionIdx = 0
try:
	with open(filePath, 'r') as f:
		content = f.read()
		optionIdx = int(content)
except:
	pass
with open(filePath, 'w+') as f:
	f.write(
		str((optionIdx + 1) % len(params[cmd]))
	)


if (cmd == 'center'):
	heightFactor = params[cmd][optionIdx]
	widthFactor = 0.75 if (heightFactor == 1) else 0.5
	w = widthFactor * width
	h = heightFactor * height
	x = (w - width) * 0.5
	y = (h - height) * 0.5
	printCombined([
		removeMaximized,
		makeResizeCmd([0, x, y, w, h]),
		# addMaximizedVert if (heightFactor == 1) else ''
	])

elif (cmd == 'maximize'):
	print(addMaximized)

elif (cmd == 'right'):
	widthFactor = params[cmd][optionIdx]
	w = widthFactor * width
	h = height
	x = width - w
	y = 0
	printCombined([
		removeMaximized,
		makeResizeCmd([0, x, y, w, h]),
		# addMaximizedVert,
	])

elif (cmd == 'left'):
	widthFactor = params[cmd][optionIdx]
	w = widthFactor * width
	h = height
	x = 0
	y = 0
	printCombined([
		removeMaximized,
		makeResizeCmd([0, x, y, w, h]),
		# addMaximizedVert,
	])
