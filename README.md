Visual AutoDrive: A Unified Demo System for Autonomous Driving

The project is composed of several parts: PC, Raspberry Pi, Arduino, Android App, model vehicle, and playground. On model vehicle, arduino controls servor for running, which is controlled by App on cell phone. The pi camera and three ultrasonic sensors are connected to Raspberry Pi, obtaining data and send them to PC via Raspberry Pi through wifi. The PC processes the streaming images and distance data from sensors in real time and visualize on the screen, and saves as video at meantime.

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
* there are three mode: video processing (input.mp4), image set processing (cityscape), and wifi streaming video from remote camera on vehicle

* to use video processing mode, add your video named as input.mp4 or specify with argument

* to use image set processing mode, download the dataset of cityscape into directory cityscape/

* to use wifi streaming mode, all the socket id for both PC and Raspberry Pi side should use same ip address on PC.

* to look up the ip address, open a terminal and type ipconfig with ENTER
```
czm@czm:~$ ifconfig
```
The ip address in wlp5s0 after inet or similar should be the right one.

* more details can be found in Usage below


## Usage:

### Main file
* open a terminal, go into project directory and run main.py on PC
* for first time, run main.py --help for details
```
python main.py --help
```
you will see
```
czm@czm:~/Visual_AutoDrive$ python main.py --help
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
```
#### Ultrasonic sensor:
* measuring & data storage (csv):
	- open a terminal and run ultrasonic_server_test_save.py on PC
	- open a terminal and run ultrasonic_client.py on Raspberry Pi

* measuring & real-time visualization:
	- open a terminal and run ultrasonic_server_test.py on PC
	- open a terminal and run ultrasonic_client.py on Raspberry Pi

#### Record Video via Pi camera:
* open a terminal and run record_video_file.py on Raspberry Pi

#### Real-time video processing and visualization:
- open a terminal and run stream_server_test.py on PC
- open a terminal and run stream_client.py on Raspberry Pi

#### Arduino code 
- arduino/bluetooth_control.ino

#### Android App
- arduino/controller.apk

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
