from operator import concat
import ffmpeg


ffmpeg.input('paths.txt',f='concat',safe=0).output('output.mp4',c='copy',framerate=2).run()

#ffmpeg -y -r 1/5 -f concat -safe 0 -i "paths.txt" -c:v libx264 -vf "fps=2,format=yuv420p" "out.mp4"

#command = f'ffmpeg -y -r 1/5 -f concat -safe 0 -i "paths.txt" -c:v libx264 -vf "fps=2,format=yuv420p" "out.mp4"'
#status, output = subprocess.getstatusoutput(command)