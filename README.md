This is the instruction on using code on PC, Raspberry Pi, and Arduino for different purpose.

## Dependencies:
* PC
	- numpy
	- socket
	- cv2
	- PIL
	- moviepy
	- keras
	- tensorflow

* Raspberry Pi
	- picamera
	- csv
	- numpy
	- RPi
	- matplotlib

## Tips
* to use wifi streaming mode, all the socket id for both PC and Raspberry Pi side should use same ip address on PC.

* to look up the ip address, open a terminal and type ipconfig with ENTER
'''
czm@czm:~$ ifconfig
'''
The ip address in wlp5s0 after inet or similar should be the right one.

* download the dataset of cityscape into directory cityscape/

## Usage:

### Main file
* open a terminal, go into project directory and run main.py on PC
* for first time, run main.py --help for details
'''
python main.py --help
'''
you will see
'''
czm@czm:~/CapStone/Capstone$ python main.py --help
Using TensorFlow backend.
usage: main.py [-h] [-v VIDEO_PATH] [-i IMG_PATH] if_seg if_video

CapStone Project: A Unified Demo System for Autonomous Driving

positional arguments:
  if_seg                set segmentation mode, 1 for semantic segmentation, 0
                        for object and lane detection
  if_video              set source processing mode, 1 for video, 0 for image
                        set, -1 for wifi streaming

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO_PATH, --video_path VIDEO_PATH
                        path to video file, defaults to demo video: input.mp4
  -i IMG_PATH, --img_path IMG_PATH
                        path to imgs dir, defaults to cityscape dir:
                        cityscape/
'''
#### Ultrasonic sensor:
measuring & data storage (csv):

open a terminal and run ultrasonic_server_test_save.py on PC

open a terminal and run ultrasonic_client.py on Raspberry Pi

measuring & real-time visualization:
open a terminal and run ultrasonic_server_test.py on PC
open a terminal and run ultrasonic_client.py on Raspberry Pi

#### Record Video via Pi camera:
open a terminal and run record_video_file.py on Raspberry Pi

#### Real-time video processing and visualization:
open a terminal and run stream_server_test.py on PC
open a terminal and run stream_client.py on Raspberry Pi

#### Arduino code 
arduino/bluetooth_control.ino

#### Android App
arduino/controller.apk

## Acknowledgement
This work is built upon the following great projects:
* [Enet](https://github.com/TimoSaemann/ENet)
	- Enet: The state-of-the-art real-time semantic segmentation framework 
	- Caffe implementation
* [YAD2K](https://github.com/allanzelener/YAD2K)
	- YOLO v2: The state-of-the-art real-time object recognition framework 
	- Keras implementation
* [MLND-Capstone](https://github.com/mvirgo/MLND-Capstone)
	- Lane detection with deep learning
* [AutoRCCar](https://github.com/hamuchiwa/AutoRCCar)
	- OpenCV Python Neural Network Autonomous RC Car
