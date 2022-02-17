#!/usr/bin/env bash

# $1 path
# $2 color path ex: assets/thumbnail/blue_green.png


convert "$2" -font Impact -fill white -pointsize 170 -gravity west -draw "text 80,0 'ELIZABETH II'" "$1/thumbnail.png"