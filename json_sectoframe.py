import json
import copy
from operator import itemgetter

def secs_to_frames():
	newfile = open("/home/alanturner/Documents/Sc1_MID_Act.json")
	new = json.load(newfile)
	newfile.close()

	annotations = new["annotations"]
	#del new["annotations"]
	for anno in annotations:
		#tmp = copy.deepcopy(anno["START - STOP"])
		#anno["START - STOP"] = tmp
		tmp = [int(anno["START - STOP"][0] * 30), int(anno["START - STOP"][1] * 30)]
		#tmp.append(int(anno["START - STOP"][0] * 30))
		#tmp.append(int(anno["START - STOP"][1] * 30))
		anno["frames"] = tmp

	new["annotations"] = sorted(annotations, key = itemgetter("vid"))
	with open("frames_sc1_mid", "w") as write_file:
		json.dump(new, write_file)

secs_to_frames()