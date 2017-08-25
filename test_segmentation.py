#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script visualize the semantic segmentation of ENet.
"""
import os
import numpy as np
import sys
caffe_root = '/home/czm/CapStone/Capstone/ENet/caffe-enet/'  # Change this to the absolute directory to ENet Caffe
sys.path.insert(0, caffe_root + 'python')
import caffe
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

def seg_enet(net, input_image, label_colours, input_shape, output_size):

    input_image = cv2.resize(input_image, (input_shape[3], input_shape[2]))
    input_image = input_image.transpose((2, 0, 1))
    input_image = np.asarray([input_image])

    out = net.forward_all(**{net.inputs[0]: input_image})

    prediction = net.blobs['deconv6_0_0'].data[0].argmax(axis=0)

    prediction = np.squeeze(prediction)
    prediction = np.resize(prediction, (3, input_shape[2], input_shape[3]))
    prediction = prediction.transpose(1, 2, 0).astype(np.uint8)

    prediction_rgb = np.zeros(prediction.shape, dtype=np.uint8)
    label_colours_bgr = label_colours[..., ::-1]
    cv2.LUT(prediction, label_colours_bgr, prediction_rgb)

    return cv2.resize(np.asarray(prediction_rgb), output_size, interpolation = cv2.INTER_CUBIC)





