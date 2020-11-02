import cv2
import numpy as np

size = (855, 250)
vid_in  = cv2.VideoCapture('Sc2b_Tk3_CAM12-h264-1.mp4')
vid_out = cv2.VideoWriter('cam12_cropped.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

while True:
	ret, frame = vid_in.read()
	if not ret: 
		break
	cropped_frame = frame[0:249, 0:854].copy()
	vid_out.write(cropped_frame)

vid_in.release()
vid_out.release()