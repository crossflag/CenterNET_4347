import sys
import os
import re
import subprocess

rootdir = "/home/alanturner/centerNet-deep-sort/MID"

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		text = os.path.join(subdir, file)
		vid_regex = "(Sc[0-9][a-z]*_Tk[0-9].*mp4$)"
		video = re.search(vid_regex, text)
		if video is not None:
			vidpath = os.path.join(rootdir, video.group())
			subprocess.call(" python centernet_deepsort2.py " + vidpath, shell=True)