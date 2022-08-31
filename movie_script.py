# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 12:05:05 2021

@author: Sergio Lopez from the John Innes Centre Bioimaging Facility

This scripts registers FLIM images obtained from a Stellaris 8 microscope and makes a video out of them.

"""

# Imports the necessary libraries.
from skimage import io, color, img_as_ubyte, transform
from pystackreg import StackReg
import numpy as np
import cv2
import os

# Imports the images.
img_2_47 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/2_47.tif')
img_3_00 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/3_00.tif')
img_3_18 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/3_18.tif')
img_3_35 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/3_35.tif')
img_3_52 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/3_52.tif')
img_4_10 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/4_10.tif')
img_4_36 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/4_36.tif')
img_4_52 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/4_52.tif')
img_5_05 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/5_05.tif')
img_5_13 = io.imread('U:/Lauren movie/new_scale (2-4 ns)/5_13.tif')

# Adds the images to a list.
list_images = [img_2_47,img_3_00,img_3_18,img_3_35,img_3_52,img_4_10,img_4_36,img_4_52,img_5_05,img_5_13]
time = [0,13,31,48,65,83,109,125,138,146] # time in minutes.

# Transforms the images from RGBA to RGB.
for i in range(len(list_images)):
    list_images[i] = color.rgba2rgb(list_images[i])

# Eliminates the white lines on the images.
for i in range(len(list_images)):
    list_images[i] = list_images[i][5:510,5:510,:]
    
# Moves certain images to the right.
for i in range(3,len(list_images)):
    tform = transform.AffineTransform(translation=(-60,0))
    list_images[i] = transform.warp(list_images[i],tform)

# Creates the registrator.
sr = StackReg(StackReg.TRANSLATION)

# Creates a copy of the list of images that will be registered.
images_reg = []
for i in range(len(list_images)):
    images_reg.append(np.copy(list_images[i]))

# Registers the images.
for i in range(len(images_reg)-1):
    sr.register(images_reg[i][:,:,0], images_reg[i+1][:,:,0])
    images_reg[i+1][:,:,0] = sr.transform(images_reg[i+1][:,:,0])
    images_reg[i+1][:,:,1] = sr.transform(images_reg[i+1][:,:,1])
    images_reg[i+1][:,:,2] = sr.transform(images_reg[i+1][:,:,2])

# Transforms the images into BGR for OpenCV.
for i in range(len(images_reg)):
    images_reg[i] = cv2.cvtColor(img_as_ubyte(np.clip(images_reg[i],0,1)),cv2.COLOR_RGB2BGR)
    
# Instanciates a VideoWriter object.
video = cv2.VideoWriter('uncompressed.avi', 0, 1, (505, 505)) # Previous codec was cv2.VideoWriter_fourcc(*'MP42') instead of "0".

# Sets the font type for OpenCV.
font = cv2.FONT_HERSHEY_SIMPLEX

# Creates the video and writes the timestamps into it.
for i in range(len(images_reg)):
    cv2.putText(images_reg[i], str(time[i])+' min', (20,450), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(images_reg[i],(450,20),(487,25),(255,255,255),5)
    video.write(images_reg[i])
    cv2.imwrite('still_image'+str(i)+'.tiff',images_reg[i])
video.release()


