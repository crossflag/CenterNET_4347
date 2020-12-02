import os
import cv2
import numpy as np
import json
import math

#CenterNet
import sys
CENTERNET_PATH = '/home/sebastiansantana/HABANERO/centerNet-deep-sort/CenterNet/src/lib'
sys.path.insert(0, CENTERNET_PATH)
from detectors.detector_factory import detector_factory
from opts import opts


#MODEL_PATH = './CenterNet/models/ctdet_coco_dla_2x.pth'
MODEL_PATH = '/home/sebastiansantana/HABANERO/centerNet-deep-sort/model_last_PROJ.pth'
ARCH = 'dla_34'
if (len(sys.argv) == 2):
    myvidpath = sys.argv[1]
    #anno_path = sys.argv[2]
    #output_path = sys.argv[3]
    #sys.exit()
else: 
    myvidpath = '/home/sebastiansantana/Documents/AIC20_track4/test-data/1.mp4'
vidout = True

#MODEL_PATH = './CenterNet/models/ctdet_coco_resdcn18.pth'
#ARCH = 'resdcn_18'



TASK = 'ctdet' # or 'multi_pose' for human pose estimation
opt = opts().init('{} --load_model {} --arch {}'.format(TASK, MODEL_PATH, ARCH).split(' '))

#vis_thresh
opt.vis_thresh = 0.7


#input_type
opt.input_type = 'vid'   # for video, 'vid',  for webcam, 'webcam', for ip camera, 'ipcam'

#------------------------------
# for video
opt.vid_path = myvidpath  #
#------------------------------
# for webcam  (webcam device index is required)
opt.webcam_ind = 0
#------------------------------
# for ipcamera (camera url is required.this is dahua url format)
opt.ipcam_url = 'rtsp://{0}:{1}@IPAddress:554/cam/realmonitor?channel={2}&subtype=1'
# ipcamera camera number
opt.ipcam_no = 8
#------------------------------


from deep_sort import DeepSort
from utilP import COLORS_10, draw_bboxes

import time
from vidgear.gears import VideoGear


def bbox_to_xywh_cls_conf(bbox):
    #confidence = 0.5
    tbb = bbox.copy()
    # Bicycle
    bbox = tbb[2]
    # Car
    bbox = np.concatenate((bbox, tbb[3]), 0)
    # Truck
    bbox = np.concatenate((bbox, tbb[8]), 0)
    # Bus
    bbox = np.concatenate((bbox, tbb[6]), 0)

    #print ("tbb: ", tbb)
    #print ("bbox: ", bbox[3])
    #exit()

    if any(bbox[:, 4] > opt.vis_thresh):
        #print(bbox)
        #exit()
        bbox = bbox[bbox[:, 4] > opt.vis_thresh, :]
        bbox[:, 2] = bbox[:, 2] - bbox[:, 0]  #
        bbox[:, 3] = bbox[:, 3] - bbox[:, 1]  #

        return bbox[:, :4], bbox[:, 4]

    else:

        return None, None


class Detector(object):
    def __init__(self, opt):
        self.vdo = cv2.VideoCapture()


        #centerNet detector
        self.detector = detector_factory[opt.task](opt)
        self.deepsort = DeepSort("deep/checkpoint/ckpt.t7")


        self.write_video = True

    def open(self, video_path):

        if opt.input_type == 'webcam':
            self.vdo.open(opt.webcam_ind)

        elif opt.input_type == 'ipcam':
            # load cam key, secret
            with open("cam_secret.txt") as f:
                lines = f.readlines()
                key = lines[0].strip()
                secret = lines[1].strip()

            self.vdo.open(opt.ipcam_url.format(key, secret, opt.ipcam_no))

        # video
        else :
            assert os.path.isfile(opt.vid_path), "Error: path error"
            self.vdo.open(opt.vid_path)
            self.stream_stab = VideoGear(source='Sc2a_Tk1_CAM12-h264-1.mp4', stabilize = True).start()

        self.im_width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.area = 0, 0, self.im_width, self.im_height
        if self.write_video:
            head_tail = os.path.split(myvidpath)
            output_vid = (head_tail[1])[:-4]
            output_vid += "_withbbox.mp4"
            print (output_vid)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.output = cv2.VideoWriter(output_vid, fourcc, 30, (self.im_width, self.im_height))
        #return self.vdo.isOpened()

    def detect(self):
        xmin, ymin, xmax, ymax = self.area
        frame_no = 0
        avg_fps = 0.0

        while self.vdo.grab():

            frame_no +=1
            _, ori_im = self.vdo.retrieve()
            im = ori_im[ymin:ymax, xmin:xmax]
            #im = ori_im[ymin:ymax, xmin:xmax, :]

            

            start = time.time()
            results = self.detector.run(im)['results']

            end_center = time.time()
            bbox_xywh, cls_conf = bbox_to_xywh_cls_conf(results)

            if bbox_xywh is not None:
                start_deep_sort =  time.time()
                outputs = self.deepsort.update(bbox_xywh, cls_conf, im)
                end_deep_sort = time.time()
                if len(outputs) > 0:
                    bbox_xyxy = outputs[:, :4]
                    identities = outputs[:, -1]
                    dists = []
                    #for box in bbox_xyxy:
                        #cx = (box[2] - box[0]) / 2
                        #cy = (box[3] - box[1]) / 2
                        #dist = math.sqrt((cx-427)**2 + (cy - 480)**2)
                        #ydist = 480 - box[3]
                        #meter_per_pix = 5.5 / abs(box[2] - box[0])
                        #dist = ydist * meter_per_pix
                        #dists.append(dist)

                    #print(dists)

                    ori_im = draw_bboxes(ori_im, bbox_xyxy, dists, identities, offset=(xmin, ymin)) #xmin, ymin
                    #print (outputs)
                    #new_detection = {}
                    #new_detection["frameNo"] = frame_no
                    #new_detection["trackID"] = identities[0]
                    #new_detection["bbox"] = bbox_xyxy
                #print("deep time: {}s".format(end_deep_sort - start_deep_sort))

            end = time.time()
            

            fps =  1 / (end - start )

            avg_fps += fps
            #print("centernet time: {}s, fps: {}, avg fps : {}".format(end_center - start, fps,  avg_fps/frame_no))

            if vidout:
                cv2.imshow("test", ori_im)
                cv2.waitKey(1)

            if self.write_video:
                self.output.write(ori_im)

if __name__ == "__main__":
    import sys
    #new_file =
    # if len(sys.argv) == 1:
    #     print("Usage: python demo_yolo3_deepsort.py [YOUR_VIDEO_PATH]")
    # else:
    if vidout:
    	cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    	cv2.resizeWindow("test", 800, 600)

    #opt = opts().init()
    det = Detector(opt)

    # det.open("D:\CODE\matlab sample code/season 1 episode 4 part 5-6.mp4")
    det.open(myvidpath)
    det.detect()
