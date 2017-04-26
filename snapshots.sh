#!/bin/bash
for filename in *.mp4 *.mov *.avi; do
    echo "$filename"
    ffmpeg -y -ss 00:00:00 -i "$filename" -vframes 1 -filter:v scale="400:-1" "$filename.png"
    ffmpeg -y -ss 00:00:01 -i "$filename" -vframes 1 -filter:v scale="400:-1" "$filename.png"
    ffmpeg -y -ss 00:00:05 -i "$filename" -vframes 1 -filter:v scale="400:-1" "$filename.png"
    ffmpeg -y -ss 00:00:15 -i "$filename" -vframes 1 -filter:v scale="400:-1" "$filename.png"
    ffmpeg -y -ss 00:00:25 -i "$filename" -vframes 1 -filter:v scale="400:-1" "$filename.png"
done
rm snapshots.sh
