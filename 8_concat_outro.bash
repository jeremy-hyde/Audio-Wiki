#!/usr/bin/env bash

# The video file and the outro must have the same parameters video (encoding, framerate, resolution, etc) and audio (encoding)

echo "file '$1/output.mp4'" > tmp_concat_list.txt
echo "file 'assets/outro/outro.mp4'" >> tmp_concat_list.txt

ffmpeg -f concat -safe 0 -i tmp_concat_list.txt -vcodec copy -acodec copy "$1/output_with_outro.mp4"

rm tmp_concat_list.txt