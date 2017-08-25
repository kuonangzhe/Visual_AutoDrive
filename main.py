#! /usr/bin/env python
__author__ = 'chongzhao mao'

# common
import numpy as np
import socket
import argparse
import colorsys
import imghdr
import os
import random
import time
import sys 
import threading 

# utility
import cv2
from PIL import ImageFont
from moviepy.editor import VideoFileClip

# caffe
caffe_root = '/home/czm/CapStone/Capstone/ENet/caffe-enet/'  # Change this to the absolute directory to ENet Caffe
sys.path.insert(0, caffe_root + 'python')
import caffe
sys.path.append('/usr/local/lib/python2.7/site-packages')

# keras
from keras import backend as K
from keras.models import load_model, model_from_json
from yad2k.models.keras_yolo import yolo_eval, yolo_head

# functions
from test_yolo2 import *
from test_segmentation import *

# param for semantic segmentation -- enet
def load_enet():
    model = 'ENet/prototxts/enet_deploy_final.prototxt'
    weights = 'ENet/enet_weights_zoo/cityscapes_weights.caffemodel'
    colours = 'ENet/scripts/cityscapes19.png'
    gpu = 0
    if gpu == 0:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()

    enet = caffe.Net(model, weights, caffe.TEST)
    
    e_input_shape = enet.blobs['data'].data.shape
    e_label_colours = cv2.imread(colours, 1).astype(np.uint8)
    return enet, e_input_shape, e_label_colours

# param for object detection -- tiny yolo
def load_yolo():
    yolo_path = 'model/yolo_model/'
    model_path = yolo_path + 'tiny_yolo_voc.h5'
    #model_path = yolo_path + 'yolo2.h5'
    anchors_path = yolo_path + 'tiny_yolo_voc_anchors.txt'
    #anchors_path = yolo_path + 'yolo_anchors.txt'
    classes_path = yolo_path + 'pascal_classes.txt'

    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]

    with open(anchors_path) as f:
        anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        anchors = np.array(anchors).reshape(-1, 2)
        print(anchors)
        #anchors = None

    yolo_model = load_model(model_path)
    print('{} model, anchors, and classes loaded.'.format(yolo_path))
    return yolo_model, anchors, class_names

# param for lane detection
def load_lane():
    lane_path = 'model/lane_model/'
    json_file = open(lane_path + 'full_CNN_model.json', 'r')
    json_model = json_file.read()
    json_file.close()
    lane_model = model_from_json(json_model)
    lane_model.load_weights(lane_path + 'full_CNN_model.h5')
    return lane_model

# set up windows
def seg_open_window():
    cv2.namedWindow('video mode')
    cv2.moveWindow('video mode', 100,100)    
    cv2.namedWindow('semantic segmentation')
    cv2.moveWindow('semantic segmentation', 1500, 100)

def det_open_window():
    cv2.namedWindow('video mode')
    cv2.moveWindow('video mode', 100,100)   
    cv2.namedWindow('object detection')
    cv2.moveWindow('object detection', 1000, 100)
    cv2.namedWindow('lane detection')
    cv2.moveWindow('lane detection', 2000, 100)

# main class for process
class VideoStreamingTest(object):
    def __init__(self,is_video, is_seg, video_path, img_path):
        self.is_video = is_video
        self.is_seg = is_seg

        self.video_path = video_path
        self.img_path = img_path
        self.output_size = tuple([1024,768])
        if (self.is_video == 0):
            self.imgs()
        elif (self.is_video > 0):
            self.video()
        else:
            self.server_socket = socket.socket()
            self.server_socket.bind(('192.168.1.103', 8000))
            self.server_socket.listen(0)
            self.connection, self.client_address = self.server_socket.accept()
            self.connection = self.connection.makefile('rb')
            self.stream()

    def imgs(self):
        
        image_list = os.listdir(self.img_path)
        image_list.sort()
        if self.is_seg:
            img_writer = cv2.VideoWriter(img_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, (2048,1024))
            img_seg_writer = cv2.VideoWriter(seg_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)
            for image_file in image_list:

                print(image_file)
                try:
                    image_type = imghdr.what(os.path.join(self.img_path, image_file))
                    if not image_type:
                        continue
                except IsADirectoryError:
                    continue
                image = cv2.imread(os.path.join(self.img_path, image_file), 1)
                cv2.imshow('video mode',image)
                img_writer.write(image)
                input_image = image.astype(np.float32)
                seg_img = seg_enet(enet, input_image, e_label_colours, e_input_shape, self.output_size)
                cv2.imshow('semantic segmentation', seg_img)
                img_seg_writer.write(seg_img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            img_seg_writer.release()
            img_writer.release()
        else:
            img_det_writer = cv2.VideoWriter(det_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)
            img_lane_writer = cv2.VideoWriter(lane_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)
            for image_file in image_list:

                print(image_file)
                try:
                    image_type = imghdr.what(os.path.join(self.img_path, image_file))
                    if not image_type:
                        continue
                except IsADirectoryError:
                    continue
                image = cv2.imread(os.path.join(self.img_path, image_file), 1)
                cv2.imshow('video mode', image)
                image = cv2.resize(image, new_image_size, interpolation = cv2.INTER_CUBIC) 
                
                det_img = obj_det(image, yolo_model, anchors, class_names, sess, font, thickness, bsc, input_image_shape, colors, self.output_size)
                cv2.imshow('object detection', det_img)
                img_det_writer.write(det_img)
                lane_img = lane_det(image, lane_model, self.output_size)
                cv2.imshow('lane detection', lane_img)
                img_lane_writer.write(lane_img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            img_lane_writer.release()
            img_det_writer.release()
            sess.close()
        cv2.destroyAllWindows()

    def video(self):
        cap = cv2.VideoCapture(self.video_path)
        if self.is_seg:
            video_seg_writer = cv2.VideoWriter(seg_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)
            while cap.isOpened():
                ret,image = cap.read()
                cv2.imshow('video mode',image)
                input_image = image.astype(np.float32)
                seg_img = seg_enet(enet, input_image, e_label_colours, e_input_shape, self.output_size)
                cv2.imshow('semantic segmentation', seg_img)
                video_seg_writer.write(seg_img)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            video_seg_writer.release()
        else: 
            video_det_writer = cv2.VideoWriter(det_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)
            #video_lane_writer = cv2.VideoWriter(lane_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)

            while cap.isOpened():
                ret,image = cap.read()
                cv2.imshow('video mode',image)
                image = cv2.resize(image, new_image_size, interpolation = cv2.INTER_CUBIC) 
                
                det_img = obj_det(image, yolo_model, anchors, class_names, sess, font, thickness, bsc, input_image_shape, colors, self.output_size)
                cv2.imshow('object detection', det_img)
                video_det_writer.write(det_img)

                lane_img = lane_det(image, lane_model, self.output_size)
                cv2.imshow('lane detection', lane_img)
                video_lane_writer.write(lane_img)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            video_det_writer.release()
            video_lane_writer.release()

            sess.close()
        cap.release()
        cv2.destroyAllWindows()
        

    def stream(self):
        try:
            print "Connection from: ", self.client_address
            print "Streaming..."
            print "Press 'q' to exit"

            stream_bytes = ' '
            if self.is_seg:
                stream_seg_writer = cv2.VideoWriter(seg_output, cv2.VideoWriter_fourcc(*'DIVX'), 25, self.output_size)
                while True:
                    stream_bytes += self.connection.read(1024)
                    first = stream_bytes.find('\xff\xd8')
                    last = stream_bytes.find('\xff\xd9')
                    if first != -1 and last != -1:
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]

                        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                        cv2.imshow('video mode',image)
                        input_image = image.astype(np.float32)
                        seg_img = seg_enet(enet, input_image, e_label_colours, e_input_shape, self.output_size)
                        cv2.imshow('semantic segmentation', seg_img)
                        stream_seg_writer.write(seg_img)
                        if cv2.waitKey(10) & 0xFF == ord('q'):
                            break
                    stream_bytes = ' '
                stream_seg_writer.release()
            else:
                while True:
                    stream_bytes += self.connection.read(1024)
                    first = stream_bytes.find('\xff\xd8')
                    last = stream_bytes.find('\xff\xd9')
                    if first != -1 and last != -1:
                        jpg = stream_bytes[first:last + 2]
                        stream_bytes = stream_bytes[last + 2:]

                        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                        frame = cv2.resize(image, new_image_size, interpolation = cv2.INTER_CUBIC) 
                        det_img = obj_det(frame, yolo_model, anchors, class_names, sess, font, thickness, bsc, input_image_shape, colors, self.output_size)
                        cv2.imshow('object detection', det_img)
                        lane_img = lane_det(frame, lane_model, self.output_size)
                        cv2.imshow('lane detection', lane_img)
                
                        if cv2.waitKey(10) & 0xFF == ord('q'):
                            break

                sess.close()
            cv2.destroyAllWindows()


        finally:
            self.connection.close()
            self.server_socket.close()






# parse the argument
parser = argparse.ArgumentParser(
    description='Visual AutoDrive: A Unified Visual Demo System for Autonomous Driving')
parser.add_argument(
    'if_seg',
    help='set segmentation mode, 1 for semantic segmentation, 0 for object and lane detection')
parser.add_argument(
    'if_video',
    help='set source processing mode, 1 for video, 0 for image set, -1 for wifi streaming')
parser.add_argument(
    '-v',
    '--video_path',
    help='path to video file, defaults to demo video: input.mp4',
    default='input.mp4')
parser.add_argument(
    '-i',
    '--img_path',
    help='path to imgs dir, defaults to cityscape dir: cityscape/',
    default='cityscape/')


if __name__ == '__main__':
    args = parser.parse_args()
    is_seg = int(args.if_seg)
    is_video = int(args.if_video)
    video_path = args.video_path
    img_path = args.img_path

    seg_output = 'result/seg_result.avi'
    det_output = 'result/det_result.avi'
    lane_output = 'result/lane_result.avi'
    img_output = 'result/video.avi'

    if is_seg:
        seg_open_window()
        # set up enet
        enet, e_input_shape, e_label_colours = load_enet()
    else:
        det_open_window()

        # set up lane detection
        lane_model = load_lane()

        # set up yolo
        yolo_model, anchors, class_names = load_yolo()

        score_threshold = 0.25
        iou_threshold = 0.4
        sess = K.get_session()
        yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))
        hsv_tuples = [(float(x) / len(class_names), 1., 1.)
                      for x in range(len(class_names))]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                colors))

        random.seed(10101)  # Fixed seed for consistent colors across runs.
        random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
        random.seed(None)  # Reset seed to default.

        model_image_size = yolo_model.layers[0].input_shape[1:3]
        new_image_size = tuple(reversed(model_image_size))
        input_image_shape = K.placeholder(shape=(2, ))
        bsc = yolo_eval(
            yolo_outputs,
            input_image_shape,
            score_threshold=score_threshold,
            iou_threshold=iou_threshold)

        image_size = [2048,1024]
        font = ImageFont.truetype(
                    font='font/FiraMono-Medium.otf',
                    size=np.floor(3e-2 * image_size[1] + 0.5).astype('int32'))
        thickness = (image_size[0] + image_size[1]) // 300
        new_image_size = tuple([416,416])

    VideoStreamingTest(is_video, is_seg, video_path, img_path)

