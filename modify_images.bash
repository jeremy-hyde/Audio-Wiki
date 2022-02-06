#!/usr/bin/env bash

#set -e

if [ ! -d "$1"/images_backup/ ]; then
    echo '=> Backup Images'
    rm
    cp -Ra "$1"/images/ "$1"/images_backup/
fi

echo '=> Recut and Insert Caption for the images'
ITER=1
for filename in "$1"/images/*; do
    line=$(sed -n "$ITER"p "$1"/images.txt)

    # Convert SVG to PNG with the right size
    if [[ $filename =~ .*\.svg ]]; then
      echo "Convert svg to png"
        # https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=31327
        filenamepng="${filename/svg/png}"
        convert -resize 1920x880 -density 400 -format png "$filename" -channel RGB "$filenamepng"
        rm "$filename"
        filename=$filenamepng
    fi

    echo $ITER
    # Shrink image to leave some space at the bottom
    convert "$filename" -resize 1920x880\> -size 1920x880 xc:black +swap -gravity center -composite "$filename"

    echo $filename
    # Add Caption with wrap at 1920 and a lot of small things
    # https://legacy.imagemagick.org/Usage/thumbnails/#labels
    convert "$filename" \( -background black -fill white -pointsize 25 -size 1920x -gravity Center caption:"$line" -trim +repage -bordercolor black -border 50 \) -gravity South -append "$filename"

    echo $line
    # Fill black to get a consistent 1920x1080 size
    convert "$filename" -resize 1920x1080\> -size 1920x1080 xc:black +swap -gravity center -composite "$filename"

    ((ITER++))
done
