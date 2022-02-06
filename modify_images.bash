
if [ ! -d "$1"/images_backup/ ]; then
    echo '=> Backup Images'
    cp -Ra "$1"/images/ "$1"/images_backup/
fi

echo '=> Recut and Insert Caption for the images'
ITER=1
for filename in "$1"/images/*; do
    line=$(sed -n "$ITER"p "$1"/images.txt)

    # Convert SVG to PNG with the right size
    if [[ $filename =~ "*.svg" ]]; then
        #[Ref](https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=31327)
        mogrify -resize 1920x880 -density 400 -format png "$1"/images/*.svg -channel RGB  "$1"/images/*.png
        rm "$1"/images/*.svg
    fi

    echo $ITER
    # Shrink image to leave some space at the bottom
    convert "$filename" -resize 1920x880\> -size 1920x880 xc:black +swap -gravity center -composite "$filename"

    echo $filename
    # Add Caption with wrap at 1920 and a lot of small things
    convert "$filename" \( -background black -fill white -pointsize 25 -size 1920x -gravity Center caption:"$line" -trim +repage -bordercolor black -border 50 \) -gravity South -append "$filename"

    echo $line
    # Fill black to get a consistent 1920x1080 size
    convert "$filename" -resize 1920x1080\> -size 1920x1080 xc:black +swap -gravity center -composite "$filename"

    ((ITER++))
done
