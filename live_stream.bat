@echo off
setlocal

:: Delete old TS segments
del *.ts >nul 2>&1

:: === Load .env file ===
(for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    call set "%%A=%%B"
))

:: === Show loaded variables ===
echo USERNAME: %CAMERA_USERNAME%
echo PASSWORD: %CAMERA_PASSWORD%
echo IP      : %CAMERA_IP%
echo PATH    : %LIVE_PATH%
echo OUTPUT  : %CAMERA_OUTPUT%

:: === Run FFmpeg with the variables ===
ffmpeg -v verbose -i rtsp://%CAMERA_USERNAME%:%CAMERA_PASSWORD%@%CAMERA_IP%/%LIVE_PATH% ^
-vf scale=1920:1080 -vcodec libx264 -r 25 -b:v 1000000 -crf 31 -acodec aac ^
-sc_threshold 0 -f hls -hls_time 5 -segment_time 5 -hls_list_size 5 %CAMERA_OUTPUT%

:: Loop back and restart
goto :start
