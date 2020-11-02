import sys
import os
import re
import subprocess

rootdir = "/home/alanturner/centerNet-deep-sort/MID"

for subdir, dirs, files in os.walk(rootdir):
	#print ("In " + os.path.join(subdir))
	vidfile_found = False
	annofile_found = False
	already_processed = False
	vidpath = ""
	annopath = ""
	for file in files:
		text = os.path.join(subdir, file)
		vid_regex = "(Sc[0-9][a-z]*_Tk[0-9].*mp4$)"
		anno_regex = "(Sc[0-9][a-z]*_Tk[0-9].*/Sc[0-9][a-z]*_Tk[0-9].*json$)"
		merge_regex = "(Sc[0-9][a-z]*_Tk[0-9].*_merged.json$)"
		video = re.search(vid_regex, text)
		annos = re.search(anno_regex, text)
		merged = re.search(merge_regex, text)
		if video is not None:
			#print (video.group())
			vidfile_found = True
			vidpath = os.path.join(rootdir, video.group())
		if annos is not None:
			#print (annos.group())
			annofile_found = True
			annopath = os.path.join(rootdir, annos.group())
		if merged is not None:
			already_processed = True
		#print ("after loop, ff = " + str(files_found))

	if vidfile_found and annofile_found:
		if not already_processed:
			output_dest = annopath[:-5] + "_merged.json"
			#print ("dest: " + output_dest)
			#os.system("/home/alanturner/centerNet-deep-sort/our_centernet_deepsort.py " + vidpath + " " + annopath + " " + output_dest)
			subprocess.call(" python our_centernet_deepsort.py " 
			             + vidpath + " " + annopath + " " + output_dest, shell=True)
		else:
			print ("Skipped " + vidpath + "; already processed")