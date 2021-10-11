import cv2
import glob
import numpy as np
import re
import base64
import os
#inputvideoname="D:/GitHub/CSC2004-Assignment1/Video/10.mp4"
inputvideoname="D:/GitHub/CSC2004-Assignment1/Video/file_example_AVI_480_750kB.avi"
outputvideoname="D:/GitHub/CSC2004-Assignment1/TEST.avi"

vidcap=cv2.VideoCapture(inputvideoname)
fps=vidcap.get(cv2.CAP_PROP_FPS)
print(fps)
success,image = vidcap.read()
count=0
# splice video to frames
while success:
    cv2.imwrite("D:/GitHub/CSC2004-Assignment1/output/random/%d.png"%count,image)
    success,image=vidcap.read()
    count+=1

# stiches frames to video
img_array = []
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

for filename in sorted(glob.glob("D:/GitHub/CSC2004-Assignment1/output/random/*.png") , key=numericalSort):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

out = cv2.VideoWriter('TEST.avi',cv2.VideoWriter_fourcc(*'RGBA'), fps, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

#decode video
vidcap=cv2.VideoCapture(outputvideoname)
fps=vidcap.get(cv2.CAP_PROP_FPS)
print(fps)
success,image = vidcap.read()
count=0
# splice video to frames
while success:
    cv2.imwrite("D:/GitHub/CSC2004-Assignment1/output/random2/%d.png"%count,image)
    success,image=vidcap.read()
    count+=1