#!/usr/bin/env bash


ffmpeg \
-f lavfi -i color=c=black:s=1920x1080:d=12 \
-i assets/outro/outro.wav \
-i assets/outro/outro.png \
-filter_complex "overlay=enable='between(t,0,12)'" \
-c:a aac \
-pix_fmt yuvj422p \
outro.mp4
