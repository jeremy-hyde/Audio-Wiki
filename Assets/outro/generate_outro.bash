#!/usr/bin/env bash


ffmpeg \
-f lavfi -i color=c=black:s=1920x1080:d=12 \
-i var/static/outro.wav \
-i var/static/outro.png \
-filter_complex "overlay=enable='between(t,0,12)'" \
-c:a aac \
-pix_fmt yuvj422p \
out.mp4
