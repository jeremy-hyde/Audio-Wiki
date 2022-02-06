

echo '=> Backup Images'
cp -Ra "$1"/images/ "$1"/images_backup/

echo '=> Convert SVG to PNG with the right size'
#[Ref](https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=31327)
mogrify -resize 1920x880 -density 400 -format png "$1"/images/*.svg -channel RGB  "$1"/images/*.png
rm "$1"/images/*.svg

echo '=> Recut and Insert Caption for the images'
echo '1. Shrink images larger than 1920x880 to less than 1920x880'
for filename in "$1"/images/*; do
    echo $filename
    convert "$filename" -resize 1920x880\> "$filename"
done

#2. Border to image
#3. fill black to size "1920 x 1080"
#4. Add caption under
