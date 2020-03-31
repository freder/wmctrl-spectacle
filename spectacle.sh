#/bin/bash

mode=$1
# maximize
# center
# right
# left

RESO=`xrandr --current | grep '*'`
cmd=`python spectacle.py "$RESO" "$mode"`
echo $cmd
eval $cmd
