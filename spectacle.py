#!/usr/bin/env python3
import sys
import re
import os


removeMaximized = 'wmctrl -r :ACTIVE: -b remove,maximized_vert,maximized_horz'
addMaximized = 'wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz'
addMaximizedVert = 'wmctrl -r :ACTIVE: -b add,maximized_vert'

params = {
	'maximize': [None],
	'center': [1.0, 0.7],
	'left': [0.33, 0.5, 0.75],
	'right': [0.33, 0.5, 0.75],
}



def commaSeparated(arr):
	return ','.join([
		str(int(a)) for a in arr
	])



def makeResizeCmd(dims):
	return 'wmctrl -r :ACTIVE: -e \'{}\''.format(
		commaSeparated(dims)
	)



def combineCommands(cmds):
	return ' ; '.join(cmds)


def parseSizeOffset(s):
	width, height, offsetX, offsetY = list(
		map(int, re.split('[x+-]', s))
	)
	return {
		'width': width,
		'height': height,
		'offsetX': offsetX,
		'offsetY': offsetY,
	}


def parseScreen(item):
	return parseSizeOffset( 
		item.split('connected ')[1].split(' ')[0]
	)


def parseScreens(screensStr):
	screens = map(
		lambda line: line.replace('primary ', ''), 
		args[0].strip('|').split('|')
	)
	screens = [
		parseScreen(item)
		for item in screens
	]
	return sorted(
		screens,
		key=lambda item: item['offsetX']
	)


def parseWindow(s):
	ret = {
		'width': 0,
		'height': 0,
		'offsetX': 0,
		'offsetY': 0,
	}
	s = s.split('|')
	for line in s:
		line = line.strip()
		parts = line.split(': ')
		if len(parts) != 2:
			continue
		parts[1] = int(parts[1])
		if parts[0] == 'Width':
			ret['width'] = parts[1]
		elif parts[0] == 'Height':
			ret['height'] = parts[1]
		if parts[0] == 'Absolute upper-left X':
			ret['offsetX'] = parts[1]
		if parts[0] == 'Absolute upper-left Y':
			ret['offsetY'] = parts[1]
	return ret


def getScreenIdx(screens, offsetX):
	indexed = list(
		enumerate(screens)
	)
	for i, screen in reversed(indexed):
		if offsetX >= screen['offsetX']:
			return i


def getOptionsIdx(mode):
	filePath = '/tmp/spectacle-{}.txt'.format(mode)
	optionIdx = 0
	try:
		with open(filePath, 'r') as f:
			content = f.read()
			optionIdx = int(content)
	except:
		pass
	with open(filePath, 'w+') as f:
		f.write(
			str((optionIdx + 1) % len(params[mode]))
		)
	return optionIdx



args = sys.argv[1:]

screens = parseScreens(args[0])
window = parseWindow(args[1])
mode = args[2]

# find out which screen the window is on
screenIdx = getScreenIdx(screens, window['offsetX'])
offsetX = screens[screenIdx]['offsetX']
width = screens[screenIdx]['width']
height = screens[screenIdx]['height']

optionIdx = getOptionsIdx(mode)

cmd = None
if (mode == 'center'):
	heightFactor = params[mode][optionIdx]
	widthFactor = 0.75 if (heightFactor == 1) else 0.5
	w = widthFactor * width
	h = heightFactor * height
	x = (width - w) * 0.5
	y = (height - h) * 0.5
	cmd = combineCommands([
		removeMaximized,
		makeResizeCmd([0, offsetX + x, y, w, h]),
		# addMaximizedVert if (heightFactor == 1) else ''
	])

elif (mode == 'maximize'):
	cmd = combineCommands([
		addMaximized
	])

elif (mode == 'right'):
	widthFactor = params[mode][optionIdx]
	w = widthFactor * width
	h = height
	x = width - w
	y = 0
	cmd = combineCommands([
		removeMaximized,
		makeResizeCmd([0, offsetX + x, y, w, h]),
		# addMaximizedVert,
	])

elif (mode == 'left'):
	widthFactor = params[mode][optionIdx]
	w = widthFactor * width
	h = height
	x = 0
	y = 0
	cmd = combineCommands([
		removeMaximized,
		makeResizeCmd([0, offsetX + x, y, w, h]),
		# addMaximizedVert,
	])

print(cmd)
os.system(cmd)
