''' Convert a video in separate images

simple app

'''

import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import os
from glob import glob

from datetime import date

os.chdir(os.path.dirname(os.path.abspath(__file__))) # change work directory to..

# ------------------S E T T I N G S---------------------------------------
path_video_source = '00_RAW_VIDEO/'
path_images_target = '01_IMAGE'

frame_mod = 10 # 

resize_image = True
img_target_size = (1280,720) # (480,272)  (640, 360)

# ----------------- Video file -----------------------------------------
force_counter = 0
for cnt, vid in enumerate(glob(os.path.join(path_video_source, '*.mp4'))):  # <--- FILE extension
    cnt = cnt + force_counter
    file_nr = str(cnt).zfill(3)  # unique handler..
    print('[INF]File nr:{:s} -> {:s}'.format(file_nr, vid))
    
    vid_file_cap = cv2.VideoCapture(vid) # open video file

    if (vid_file_cap.isOpened() == False):
        print(f'[ERR]Open video file. File {vid} available?')

    frame_counter = 0
    
    while(vid_file_cap.isOpened()):
        ret, frame = vid_file_cap.read() # read frame
        
        if ret == True:            
            if (frame_counter % frame_mod == 0):  # save frame?                   
                if frame.shape[0] > frame.shape[1]: # rotate frame if ...
                    frame = ndimage.rotate(frame, 90)                   
                if resize_image:    # resize frame?
                    resized_frame = cv2.resize(frame, img_target_size) # resize frame 
                # height, width = img.shape[:2]
                else:
                    resized_frame = frame    
       
                cv2.imwrite(os.path.join(path_images_target, str(date.today()) + '_' + file_nr + '_' + str(frame_counter).zfill(5) + '_video.png'), resized_frame) # save resized image
            frame_counter+=1
        else:
            print('[INF]...File finished! Frame counter:', frame_counter)
            break
    vid_file_cap.release()

print('FIN')
