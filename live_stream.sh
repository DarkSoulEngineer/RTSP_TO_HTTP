#!/bin/bash
set -x

# Load env vars
set -o allexport
source .env
set +o allexport

echo "USERNAME: $CAMERA_USERNAME"
echo "PASSWORD: $CAMERA_PASSWORD"
echo "IP      : $CAMERA_IP"
echo "PATH    : $LIVE_PATH"
echo "OUTPUT  : $CAMERA_OUTPUT"

rm -f *.ts

echo "Running FFmpeg with URL:"
echo "rtsp://$CAMERA_USERNAME:$CAMERA_PASSWORD@$CAMERA_IP/$LIVE_PATH"

ffmpeg -v verbose -i "rtsp://$CAMERA_USERNAME:$CAMERA_PASSWORD@$CAMERA_IP/$LIVE_PATH" -vf scale=1920:1080 -vcodec libx264 -r 25 -b:v 1000000 -crf 31 -acodec aac -sc_threshold 0 -f hls -hls_time 5 -segment_time 5 -hls_list_size 5 "$CAMERA_OUTPUT"
