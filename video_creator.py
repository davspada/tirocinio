from operator import concat
import subprocess
import ffmpeg


command = ffmpeg.input('paths.txt',f='concat',safe=0).output('output.mkv',c='libx264').run() #, vf='fps=2'in output

#ffmpeg -y -r 1/5 -f concat -safe 0 -i "paths.txt" -c:v libx264 -vf "fps=2,format=yuv420p" "out.mp4"