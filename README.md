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
* All the socket id for on both PC and Raspberry Pi side should use ip address on PC.
To look up the ip address, open a terminal and type ipconfig with ENTER, the ip address in wlp5s0 after inet or similar should be the right one.

* Download the dataset of cityscape into directory cityscape/

## Usage:

### Main file
open a terminal and run main.py on PC
for first time, run main.py --help for details

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
arduino/arduino_bluetooth_control.ino

#### Android App
arduino/controller.apk

## Acknowledgement
This work is built upon the following great projects:
* [Enet](https://github.com/TimoSaemann/ENet)
	- The state of the art real time semantic segmentation framework Enet
	- Caffe implementation
* [YAD2K](https://github.com/allanzelener/YAD2K)
	- The state of the art real time object recognition framework YOLO v2
	- Keras implementation
* [MLND-Capstone](https://github.com/mvirgo/MLND-Capstone)
	- Lane detection with deep learning
* [AutoRCCar](https://github.com/hamuchiwa/AutoRCCar)
	- OpenCV Python Neural Network Autonomous RC Car
