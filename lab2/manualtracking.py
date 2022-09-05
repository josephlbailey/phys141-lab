#!/usr/bin/env python3
"""
Created on Fri Jul 10 10:46:00 2020

@author: Wolg
"""
"""
This file contains two functions. The first is ReadFrame which
reads a specific frame from a video file.  The second is called 
TrackMotion. This function tracks the largest object in the image 
that is darker than the background. The TrackMotion function also
assumes that there are scale markers included in the image that the 
user will click on during the first frame to define the pixel to cm 
ratio.  The distance between these markers should be input in cm.
"""

import argparse
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Recording and Analyzing Moving Objects',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        help='Input video file',
                        type=str)


    parser.add_argument('-d',
                        '--dist',
                        metavar='distance',
                        help='Distance',
                        type=float,
                        default=5)

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'Invalid file "{args.file}"')

    return args

# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    x_cm, y_cm, time = track_motion(args.file, args.dist)

    print(f'X = "{x_cm}", Y = "{y_cm}", time = "{time}"')

# --------------------------------------------------
def ReadFrame(VidObj,FrameNum):
    
    VidObj.set(1,FrameNum)
    
    ret,frame = VidObj.read()
    
    return frame

# --------------------------------------------------
def track_motion(Filename,Dist):
    
    VidObj = cv2.VideoCapture(Filename)
    
    # determine the size of the video images and the number of frames
    Width = VidObj.get(3)
    Height = VidObj.get(4)
    FPS = VidObj.get(5)
    NumFrames = int(VidObj.get(7)) # determines number of frames in video
    
    # setup arrays to store the coordinates 
    # of the center of mass at each time point
    Xcm = np.zeros((NumFrames,1))
    Ycm = np.zeros((NumFrames,1))
    
    # define the time of each frame
    Time = np.array([i for i in range(NumFrames)],dtype='float')/FPS
    
    # read in first frame and convert to float
    
    frame = ReadFrame(VidObj,0)
    
    # convert frame to RGB from BGR
    frame = frame[:,:,[2,1,0]]
    
    # have user measure the distance between lines in image
 
    fig = plt.figure()
    plt.imshow(frame)
    fig.suptitle('Click on two marker positions in the image that are Dist apart.')
    points = np.array(plt.ginput(2))

    # define the pixel to cm scale
    dis = np.sqrt((points[1,0] - points[0,0])**2 + (points[1,1] - points[0,1])**2) 
    Pix2cm = Dist/dis
    
    # loop through the remaining frames in the video
    for i in range(NumFrames):
    
        # read in frame   
        frame = ReadFrame(VidObj,i)
    
        # convert frame to RGB from BGR
        frame = frame[:,:,[2,1,0]]
    
        # have user determine center of object in image  
        plt.cla()
        fig.suptitle('Click on the center of the object')
        plt.imshow(frame)
    
        # find the Center of Mass of the object
        CM = np.array(plt.ginput(1))
        Xcm[i] = CM[0,0]
        Ycm[i] = CM[0,1]
        
        print(Xcm[i],Ycm[i])
    
        # plot the mask and its center of mass
        plt.plot(Xcm[i],Ycm[i],'or')
        plt.pause(0.1)
        
    # convert Xcm and Ycm to centimeters
    Xcm = Pix2cm*Xcm
    Ycm = Pix2cm*Ycm
        
    # plot Xcm vs. time
    plt.figure()
    plt.plot(Time,Xcm)
    plt.xlabel('Time (s)',fontname='Arial',fontsize=16)
    plt.ylabel('Distance (cm)',fontname='Arial',fontsize = 16)
    
    VidObj.release()
    
    return Xcm,Ycm,Time

# --------------------------------------------------
if __name__ == '__main__':
    main()