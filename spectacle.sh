#/bin/bash

cmd=$1
# maximize
# center
# right
# left

RESO=`xrandr | grep '*'`
python spectacle.py "$RESO"
