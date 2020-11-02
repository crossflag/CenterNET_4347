# import libraries
from vidgear.gears import VideoGear
import numpy as np
import cv2
import time

options = {'SMOOTHING_RADIUS': 50, 'BORDER_SIZE': 0, 'CROP_N_ZOOM' : True,  'BORDER_TYPE': 'black'}

stream_stab = VideoGear(source='Sc2b_Tk3_CAM14-h264-1_withbbox.mp4', stabilize = True).start() # To open any valid video stream with `stabilize` flag set to True.
stream_org = VideoGear(source='Sc2b_Tk3_CAM14-h264-1_withbbox.mp4').start() # open same stream without stabilization for comparison

# infinite loop
while True:
  start = time.time()

  frame_stab = stream_stab.read()
  # read stabilized frames

  # check if frame is None
  if frame_stab is None:
    #if True break the infinite loop
    break
  
  #read original frame
  frame_org = stream_org.read()

  #concatenate both frames
  output_frame = np.concatenate((frame_org, frame_stab), axis=1)

  #put text
  cv2.putText(output_frame, "Before", (10, output_frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
  cv2.putText(output_frame, "After", (output_frame.shape[1]//2+10, output_frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
  
  cv2.imshow("Stabilized Frame", output_frame)
  # Show output window

  key = cv2.waitKey(1) & 0xFF
  # check for 'q' key-press
  if key == ord("q"):
    #if 'q' key-pressed break out
    break

  end = time.time()
  total = end - start
  fps = 1 / total
  print ("FPS: ", fps)

cv2.destroyAllWindows()
# close output window
stream_org.stop()
stream_stab.stop()
# safely close video streams.