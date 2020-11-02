import json
import cv2
#Takes in basic video
cap = cv2.VideoCapture('IPATCH-Sc2a_Tk1_TST_Th2.mp4')
#Reads in via format and removes junk leaving just annotations.
def remove_junk():
    newfile = open("/home/sebastiansantana/Documents/iPATCH_VIA/MID/Sc1/VIA/via_project_MID_Sc1.json")
    new = json.load(newfile)
    newfile.close()

    metadata = new["metadata"]
    dictlist = []
    del new["metadata"]
    del new['project']
    del new['config']
    for key, value in metadata.items():
        dictlist.append(value)
        # time = metadata["z"]
    new["annotations"] = dictlist
    new_anno = new["annotations"]

    with open('list.json','w') as f:
	    json.dump(new, f)


#Reformats vid_id
def vid_id():
    old_file = open ('list.json')
    old = json.load(old_file)
    old_file.close()

    vid_coco=[]

    for index, file in old['file'].items():
        vid = {}
        vid = file
        #Reads in the Resolution and Frame rate sing cv
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        vid["fid"] = int(vid["fid"])
        vid["Width"] = w
        vid["Height"] = h
        vid["FPS"] = fps
        del vid["src"]
        del vid["loc"]
        del vid["type"]
        vid_coco.append(vid)

    old["file"] = vid_coco
    old['videos'] = old.pop('file')
    with open('test.json','w') as f:
        json.dump(old,f)

def Anno_Format():
    new_file = open('test.json')
    new = json.load(new_file)
    new_file.close()
    count = 0
    for dictList in new['annotations']:
        dictList["vid"] = int(dictList["vid"])
        dictList["START - STOP"] = dictList.pop("z")

    with open('test.json', 'w') as f:
        json.dump(new,f)

def categories():
    new_file = open('test.json')
    dictList = json.load(new_file)
    new_file.close()
    count = 0
    activities = []
    for  key, value in dictList['attribute']['1']['options'].items():
        new = {}
        new['supercategory'] = 'boat-boat'
        new['id'] = count
        count += 1
        new['name'] = value
        activities.append(new)
    dictList['activites'] = activities
    del dictList['attribute']
    del dictList['view']

    with open('test.json', 'w') as f:
        json.dump(dictList,f)

def fixing_via_dictlist():
    new_file = open('test.json')
    dictList = json.load(new_file)
    new_file.close()
    count = 0
    for anno in dictList['annotations']:
        if anno['av']['1'] == "follow":
            anno['activity_id'] = 2
        if anno['av']['1'] == "Speed up":
            anno['activity_id'] = 0
        if anno['av']['1'] == "speed up":
            anno['activity_id'] = 0
        if anno['av']['1'] == "loiter":
            anno['activity_id'] = 1
        if anno['av']['1'] == "seperate":
            anno['activity_id'] = 3
        if anno['av']['1'] == "merge":
            anno['activity_id'] = 4
        if anno['av']['1'] == "circling":
            anno['activity id'] = 5
        if anno['av']['1'] == "approaching":
            anno['activity id'] = 6
        del anno['flg']
        del anno['av']
        anno['id'] = count
        count += 1

    with open('Sc1_MID_Act.json', 'w') as f:
        json.dump(dictList,f)

remove_junk()
vid_id()
Anno_Format()
categories()
fixing_via_dictlist()
