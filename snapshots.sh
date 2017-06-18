#!/bin/bash
for filename in *.mp4 *.mov *.avi; do
    echo "$filename"
    ffmpeg -y -ss 00:01:00 -i "$filename" -vframes 1 -filter:v scale="320:180" "$filename.png"
done
