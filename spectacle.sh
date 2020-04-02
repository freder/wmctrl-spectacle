#/bin/bash

# maximize | center | right | left
mode=$1

# get info about connected screens
# example:
# DVI-D-0 connected 1920x1080+2560+0 (normal left inverted right x axis y axis) 477mm x 268mm
# HDMI-0 connected primary 2560x1440+0+0 (normal left inverted right x axis y axis) 553mm x 311mm
screens=`xrandr | grep ' connected ' | tr '\n' '|'`

# get active window id
# example: 117440523
winId=`xdotool getactivewindow`
window=`xwininfo -id $winId \
	| grep -e 'xwininfo: Window id:' -e 'Absolute' -e 'Width' -e 'Height' \
	| tr '\n' '|'`
# echo $window

scriptPath="$(dirname $0)/spectacle.py"
"$scriptPath" "$screens" "$window" "$winId" "$mode"
