#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2022/09/04 13:10:44

@author: josephlbailey@arizona.edu

Code can also be found at: https://github.com/josephlbailey/phys141-lab

This file contains two functions. The first is read_frame which
reads a specific frame from a video file. The second is called
track_motion. This function tracks the largest object in the image
that is darker than the background. The track_motion function also
assumes that there are scale markers included in the image that the
user will click on during the first frame to define the pixel to cm
ratio. The distance (dist) between these markers should be input in cm.
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np


def read_frame(vid_obj, frame_num):
    vid_obj.set(1, frame_num)
    ret, frame = vid_obj.read()
    return frame


def track_motion(filename, thresh, dist):
    vid_obj = cv2.VideoCapture(filename)

    # determine the size of the video images and the number of frames
    width = vid_obj.get(3)
    height = vid_obj.get(4)
    fps = vid_obj.get(5)
    num_frames = int(vid_obj.get(7))  # determines number of frames in video

    # setup arrays to store the coordinates
    # of the center of mass at each time point
    xcm = np.zeros(num_frames)
    ycm = np.zeros(num_frames)

    time = np.array([i for i in range(num_frames)], dtype='float') / fps

    # read in first frame and convert to float
    frame = read_frame(vid_obj, 0)

    # convert frame to RGB
    frame = frame[:, :, [2, 1, 0]]

    # have user measure the distance between lines in image
    fig = plt.figure()
    plt.imshow(frame)
    fig.suptitle('Click on two marker positions in the image that are Dist apart.')
    points = np.array(plt.ginput(2))

    # define the pixel to cm scale
    d = np.sqrt((points[1, 0] - points[0, 0]) ** 2 + (points[1, 1] - points[0, 1]) ** 2)
    pix2cm = dist / d

    # loop through the remaining frames of the video
    for i in range(0, num_frames):
        # read in first frame and convert to float
        frame = read_frame(vid_obj, i)
        frame = frame.astype('float')

        # compute the grayscale image
        gray = np.mean(frame, axis=2, dtype=float)
        blue = frame[:, :, 0]

        # find values of the grayscale image greater than Thresh
        mask = (blue - gray > thresh)

        # find the connected regions in the mask
        regions = cv2.connectedComponentsWithStats(mask.astype('uint8'))

        # determine which region has the largest area
        stats = regions[2]
        stats[0, 4] = 0
        can_label = np.argmax(stats[:, 4])

        # remove unwanted regions from the mask
        can_mask = mask
        can_mask[regions[1] != can_label] = 0

        # find the Center of Mass of the object
        xcm[i] = regions[3][can_label, 0]
        ycm[i] = regions[3][can_label, 1]

        # plot the mask and its center of mass
        plt.clf()
        plt.spy(can_mask)
        plt.plot(xcm[i], ycm[i], 'or')
        plt.pause(0.1)

    # convert xcm and ycm to centimeters
    xcm = pix2cm * xcm
    ycm = pix2cm * ycm

    # plot xcm as a function of time
    plt.figure()
    plt.plot(time, xcm)

    plt.xlabel('Time (s)', fontname='Arial', fontsize=16)
    plt.ylabel('Distance (cm)', fontname='Arial', fontsize=16)

    vid_obj.release()

    return xcm, ycm, time
