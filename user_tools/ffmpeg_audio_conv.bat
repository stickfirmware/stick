@echo off
echo Welcome to audio converter for Stick firmware
echo Make sure you have ffmpeg installed and configured in PATH

set /p input="Enter file name: "

ffmpeg -i "%input%" -ar 16000 -ac 1 -c:a pcm_s16le output.wav

echo Operation completed

pause