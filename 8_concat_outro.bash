#!/usr/bin/env bash

echo "file $1/output.mp4" > tmp_concat_list.txt
echo 'file assets/outro/outro.mp4' >> tmp_concat_list.txt

ffmpeg -f concat -safe 0 -i tmp_concat_list.txt -c copy "$1"/output_with_outro.mp4