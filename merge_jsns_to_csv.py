import json
import csv
import sys
import copy

def collect_activities():
	newfile = open(sys.argv[1])
	annos = json.load(newfile)
	newfile.close()
	annotations = annos["annotations"]
	videos = []

	cntr = -1
	for a in annotations:
		if a["vid"] > cntr:
			cntr += 1
			video = {}
			video["videoID"] = cntr
			video["activities"] = []
			videos.append(video)

		activity = {}
		activity["actvityID"] = a["activity_id"]
		activity["range"] = [a["frames"][0], a["frames"][1]]
		videos[cntr]["activities"].append(activity)

	return videos

def assign_acivities_to_frames():
	newfile = open(sys.argv[2])
	frames = json.load(newfile)
	newfile.close()

	videos = collect_activities()
	for v in videos:
		acts = v["activities"]
		for a in acts:
			f_range = a["range"]
			for i in f_range:
				frames[i]["activities"].append(a["actvityID"])

	with open(sys.argv[3], "w") as write_file:
		json.dump(frames, write_file)



if __name__ == "__main__":
	if len(sys.argv) < 4:
		print ("Usage: python " + sys.argv[0] + " <path_to_json_anno> <path_to_json_output> <destination_path>")
		sys.exit()

	assign_acivities_to_frames()


#/home/alanturner/centerNet-deep-sort/frames_sc1_mid
#/home/alanturner/centerNet-deep-sort/output_frames.json
#/home/alanturner/centerNet-deep-sort/merged_jsons.json