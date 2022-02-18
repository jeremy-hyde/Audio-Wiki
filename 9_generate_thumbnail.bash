#!/usr/bin/env bash

# use https://www.remove.bg/upload to remove background

PORTRAIT="$1/portrait.*"
PATTERN="$1/pattern.*"
TITLE=$2
SUBTITLE=$3
FLIP=$4
TITLE_SIZE=240
SUBTITLE_SIZE=120
TEXT_OFFSET=50

# use -flop to flip image
if [[ "$FLIP" == "flip" ]]; then
convert -verbose "$PORTRAIT" -flop "$PORTRAIT"
fi

# Resize https://legacy.imagemagick.org/Usage/resize/
convert -verbose "$PORTRAIT" -resize 1920x1080 "$1/portrait_size.png"
# Resize and fill (cut side) to size
convert -verbose "$PATTERN" -resize 1920x1080^ -gravity center -extent 1920x1080 "$1/pattern_size.png"

# Add pattern under background https://legacy.imagemagick.org/Usage/compose/
composite -dissolve 95 -gravity center assets/thumbnail/charcoal.png  "$1/pattern_size.png" -alpha Set "$1/thumbnail_bg.png"
# Add image to background https://imagemagick.org/script/composite.php
composite -verbose -gravity east "$1/portrait_size.png" "$1/thumbnail_bg.png" "$1/thumbnail.png"

# Add Title and sub title
convert -verbose "$1/thumbnail.png" \
-font Impact -fill white -pointsize $TITLE_SIZE -gravity west -draw "text $TEXT_OFFSET,0 '$TITLE'" \
-font Impact -fill white -pointsize $SUBTITLE_SIZE -gravity west -draw "text $TEXT_OFFSET,150 '$SUBTITLE'" \
"$1/thumbnail.png"
