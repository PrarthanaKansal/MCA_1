# -*- coding: utf-8 -*-
"""BlobDetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GkGG1zhhJWhbNJTRPvTLPVnV_q46QtHn
"""

from google.colab import drive
import cv2
from pylab import *
import numpy as np
import math
import matplotlib.pyplot as plt
import os
from scipy import ndimage
from scipy.ndimage import filters
from scipy import spatial
image_path = "/content/drive/My Drive/images"
drive.mount('/content/drive')
k = 1.414
sigma = 1.0

def loadImages(path):
    '''Put files into lists and return them as one list with all images 
     in the folder'''
    image_files = sorted([os.path.join(path, '', file)
                          for file in os.listdir(path)
                          if file.endswith('.jpg')])
    return image_files

def count(dir, counter=0):
    "returns number of files in dir and subdirs"
    for pack in os.walk(dir):
        for f in pack[2]:
            counter += 1
    return dir + " : " + str(counter) + "files"

def display_one(a, title1 = "Original"):
    plt.imshow(a), plt.title(title1)
    plt.show()

def display_two(img):
  cv2.imshow('image',img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def display_correct(imagePath):
  img = cv2.imread(imagePath,0)
  plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
  plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
  plt.show()

def loadQueryFolder():
  #Gives the array of all text files in the query folder
  file_content =[]
  txt_files = glob.glob("/content/drive/My Drive/train/query/*.txt")
  return txt_files

def query():
  #Takes one file from the query folder and extracts the image name
  Query = loadQueryFolder()
  listOfQueries=[]
  for i in range(len(Query)):
    with open(i, 'r') as fd:
      line = fd.readline()
      #b = line.index(" ")
      query = line
      query+=".jpg"
    
      listOfQueries.append(query)
  return listOfQueries

def LoG(sigma):
    arr = []
    mul = sigma*6
    n = ceil(mul)
    a = -n//2
    b = n//2+1
    y,x = np.ogrid[a:b,a:b]
    a = y**2
    b = x**2
    tempVar = a*b
    tempVar2 = (a*b)**2

    toDivide = 2.*sigma**2
    exp_y = a/(toDivide)
    exp_x = b/(toDivide)
    y_filter = np.exp(-(exp_y))
    x_filter = np.exp(-(exp_x))
    resultant_filter = x_filter*y_filter
    
    den = 2*np.pi*sigma**4
    final_filter = (-(2*sigma**2) + (a + b) ) *  (resultant_filter) * (1/(den))
    arr.append(final_filter)
    return final_filter


def LoG_convolve(img, factor):
    log_images = [] #to store responses
    i = 0
    while i<9:
    #for i in range(0,9):
        a = k**i
        b = a*sigma
        filter_log = LoG(b)
        #sigma_1 = sigma*y #sigma 
        #filter_log = LoG(sigma_1) #filter generation
        image = cv2.filter2D(img,factor,filter_log) # convolving image
        #print(image)
        #image = np.pad(image,((1,1),(1,1)),'constant') #padding
         
        image = np.square(image) # squaring the response
        log_images.append(image)
        i+=1
    log_image_np = np.array(log_images) # storing the #in numpy array
    return log_image_np



def detect_blob(log_image_np,img):
    co_ordinates = [] #to store co ordinates
    (h,w) = img.shape
    i = 1
    j = 1
    for i in range(1,h):
        
        for j in range(1,w):
            a = i-1
            b = a+3
            c = j-1
            d = c+3
            slice_img = log_image_np[:,a:b,c:d] #9*3*3 slice
            result = np.amax(slice_img) #finding maximum
            if result >= 0.03: #threshold
                z,x,y = np.unravel_index(slice_img.argmax(),slice_img.shape)
                x_coordinate = i+x-1
                y_coordinate = j+y-1
                z_coordinate = k**z*sigma
                co_ordinates.append((x_coordinate,y_coordinate,z_coordinate)) #finding co-rdinates
            elif result <0.03:
                pass
        #     j=j+1
        # i=i+1
    return co_ordinates

def main():
  dataset = loadImages(image_path)
  for i in range(5):
    img = cv2.imread(dataset[i],0)
    newsize = (64, 64) 
    # img = img.resize(newsize) 
    img = img/255.0
    factor = -1
    log_image_np = LoG_convolve(img,factor)
    #print(log_image_np.shape)
    #print(detect_blob(log_image_np))
    co_ordinates = list(dict.fromkeys(detect_blob(log_image_np, img))) #remove duplicates from the array by converting into set
    #co_ordinates = list(set(detect_blob(log_image_np, img))) #remove duplicates from the array by converting into set
    #print(co_ordinates)
    fig, ax = plt.subplots()
    nh,nw = img.shape
    #count = 0
    ax.imshow(img, interpolation='nearest',cmap="gray")
    for blob in co_ordinates:
        y,x,r = blob
        newRadius = r*1.414
        c = plt.Circle((x, y), newRadius, color='red', linewidth=0.8, fill=False)
        ax.add_patch(c)
    ax.plot()  
    plt.show()
    co_ordinates.clear()
  
main()

