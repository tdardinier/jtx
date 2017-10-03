#!/bin/bash

if  [ ! -d "snaps" ]; then
  mkdir snaps
fi

if  [ ! -d "sub" ]; then
  mkdir sub
fi

cd LQ

for fic in *.srt
do
    echo "$fic"
    ffmpeg -i "$fic" "$fic.vtt"
    mv "$fic.vtt" ../sub
done

for fic in *.mp4 *.avi
do

    echo "$fic"

    ffmpeg -y -ss 00:00:01 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"
    ffmpeg -y -ss 00:00:02 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"
    ffmpeg -y -ss 00:00:03 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"
    ffmpeg -y -ss 00:00:05 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"
    ffmpeg -y -ss 00:00:10 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"
    ffmpeg -y -ss 00:00:30 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"
    ffmpeg -y -ss 00:01:00 -i "${fic}" -vframes 1 -filter:v scale="320:180" "../snaps/$fic.png"

    mv "$fic" MD

done

cd ..

rm encodage_lq.sh
