#!/bin/bash

if  [ ! -d "MD" ]; then
  mkdir MD
fi

if  [ ! -d "LQ" ]; then
  mkdir LQ
fi

if  [ ! -d "snaps" ]; then
  mkdir snaps
fi

if  [ ! -d "sub" ]; then
  mkdir sub
fi

for fic in *.srt
do
    echo "$fic"
    ffmpeg -i "$fic" "$fic.vtt"
    mv "$fic" MD
    mv "$fic.vtt" sub
done

for fic in *.mp4 *.avi
do

    echo "$fic"

    ffmpeg -i "${fic}" -threads 0 -c:v libx264 -b:v 512K -r 25 -s 1280x720 -x264opts level=3.1 -pix_fmt yuv420p -c:a aac -strict experimental -b:a 192k -y "LQ/${fic}"

    ffmpeg -y -ss 00:00:01 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"
    ffmpeg -y -ss 00:00:02 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"
    ffmpeg -y -ss 00:00:03 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"
    ffmpeg -y -ss 00:00:05 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"
    ffmpeg -y -ss 00:00:10 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"
    ffmpeg -y -ss 00:00:30 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"
    ffmpeg -y -ss 00:01:00 -i "${fic}" -vframes 1 -filter:v scale="320:180" "snaps/$fic.png"

    mv "$fic" MD

done

rm encodage_mq.sh
touch encoding_proj_fini
