import subprocess

subprocess.run(["ffmpeg","-i","videos/Installing VS Code & How Websites Work _ Sigma Web Development Course - Tutorial #1 [Bjyiuej].mp4","-ss","00:00:00","-t","00:00:10","-vn","audios/sample.mp3"])