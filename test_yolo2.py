#! /usr/bin/env python3
"""Run a YOLO_v2 style detection model on test images."""
import argparse
import colorsys
import imghdr
import os
import random
import time

import cv2
import numpy as np
from keras.layers.core import K
#from keras import backend as K
from keras.models import load_model, model_from_json
from PIL import Image, ImageDraw, ImageFont

from yad2k.models.keras_yolo import yolo_eval, yolo_head

from scipy.misc import imresize

def obj_det(image, yolo_model, anchors, class_names, sess, font, thickness, bsc, input_image_shape, colors, output_size):
        image_data = np.array(image, dtype='float32')
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
        [boxes, scores, classes] = bsc
        out_boxes, out_scores, out_classes = sess.run(
            [boxes, scores, classes],
            feed_dict={
                yolo_model.input: image_data,
                input_image_shape: [image.shape[1], image.shape[0]],
                K.learning_phase(): 0
            })
        for i, c in reversed(list(enumerate(out_classes))):
            # if (c != 0 and c != 1 and c != 2 and c != 3 and c != 5 and c != 7 and c!= 9 and c!= 11):
            if (c != 1 and c != 5 and c != 6 and c != 13 and c != 14):
                continue
            predicted_class = class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)

            imagex = Image.frombytes('RGB', (416,416), image.tobytes())
            image = imagex
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)
            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            # print(label, (left, top), (right, bottom))

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=colors[c])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=colors[c])
            draw.text(text_origin, label, fill=(0, 0, 0), font=font)
            del draw
        return cv2.resize(np.asarray(image), output_size, interpolation = cv2.INTER_CUBIC)
        #image.save(os.path.join(output_path, image_file), quality=90)

class Lanes():
    def __init__(self):
        self.recent_fit = []
        self.avg_fit = []

def lane_det(image, model, output_size):
    """ Takes in a road image, re-sizes for the model,
    predicts the lane to be drawn from the model in G color,
    recreates an RGB image of a lane and merges with the
    original road image.
    """
    lanes = Lanes()
    # Get image ready for feeding into model
    small_img = imresize(image, (80, 160, 3))
    small_img = np.array(small_img)
    small_img = small_img[None,:,:,:]

    # Make prediction with neural network (un-normalize value by multiplying by 255)
    prediction = model.predict(small_img)[0] * 255

    # Add lane prediction to list for averaging
    lanes.recent_fit.append(prediction)
    # Only using last five for average
    if len(lanes.recent_fit) > 5:
        lanes.recent_fit = lanes.recent_fit[1:]

    # Calculate average detection
    lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis = 0)

    # Generate fake R & B color dimensions, stack with G
    blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
    lane_drawn = np.dstack((blanks, lanes.avg_fit, blanks))

    # Re-size to match the original image
    lane_image = imresize(lane_drawn, (image.shape[0], image.shape[1], 3))

    # Merge the lane drawing onto the original image
    result = cv2.addWeighted(image, 1, lane_image, 1, 0)

    return cv2.resize(np.asarray(result), output_size, interpolation = cv2.INTER_CUBIC)
