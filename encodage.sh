#!/bin/bash

#### UTILISATION
# Copier ce fichier dans le dossier contenant les originaux (typiquement "A cosser")
# Lancer ./encodage.sh
# C'est tout beau ! :)
####
if  [ ! -d "MQ" ]; then
  mkdir MQ
fi
for fic in *.mp4
do
  if [ -f "${fic/%.mp4/.srt}" ]; 
  then
    ffmpeg -i "${fic}" -threads 0 -c:v libx264 -b:v 3M -r 25 -s 1280x720 -x264opts level=3.1 -pix_fmt yuv420p -c:a aac -strict experimental -b:a 192k -vf subtitles="${fic/%.mp4/.srt}" -y "MQ/${fic}"
  else
    ffmpeg -i "${fic}" -threads 0 -c:v libx264 -b:v 3M -r 25 -s 1280x720 -x264opts level=3.1 -pix_fmt yuv420p -c:a aac -strict experimental -b:a 192k -y "MQ/${fic}"
  fi
done
if  [ ! -d "HQ" ]; then
  mkdir HQ
fi
mv *.mp4 HQ/
mv *.srt HQ/
mv *.sub HQ/
rm encodage.sh
