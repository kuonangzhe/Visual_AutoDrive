"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
import picamera


# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.111', 8002)) # computer's ip
connection = client_socket.makefile('wb')

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)      # pi camera resolution
        camera.framerate = 10               # 10 frames/sec
        time.sleep(2)                       # give 2 secs for camera to initilize
        start = time.time()	
        stream = io.BytesIO()
        
        # send jpeg format video stream
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
			connection.write(struct.pack('<L', stream.tell()))
            connection.flush()

            # Rewind the stream and send the image data over the wire
			stream.seek(0)
            connection.write(stream.read())+
			
			# If we've been capturing for more than 10 seconds, quit
            if time.time() - start > 10:
                break
            stream.seek(0)
            stream.truncate()
			
	# Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()