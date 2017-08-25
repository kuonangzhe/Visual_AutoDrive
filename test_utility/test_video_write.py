#! /usr/bin/env python3
import cv2
import os
import sys
import random
import time

test_path = 'cityscape/'
output = 'cityscape.avi'
image_list = os.listdir(test_path)
image_list.sort()

writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'DIVX'), 25, (2048,1024))

for image_file in image_list:
    print(image_file)
    image = cv2.imread(os.path.join(test_path, image_file), 1)
    writer.write(image)

writer.release()


