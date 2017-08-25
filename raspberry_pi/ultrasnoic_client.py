from socket import *
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)

# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8002)) #computer's ip

def measure(GPIO_TRIGGER, GPIO_ECHO):
    """
    measure distance
    """
	
	GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2

    return distance

# referring to the pins by GPIO numbers
GPIO.setmode(GPIO.BCM)

# define pi GPIO1
GPIO_TRIGGER1 = 18
GPIO_ECHO1    = 23

# output pin: Trigger
GPIO.setup(GPIO_TRIGGER1,GPIO.OUT)
# input pin: Echo
GPIO.setup(GPIO_ECHO1,GPIO.IN)
# initialize trigger pin to low
GPIO.output(GPIO_TRIGGER1, False)


# define pi GPIO2
GPIO_TRIGGER2 = 24
GPIO_ECHO2    = 25

# output pin: Trigger
GPIO.setup(GPIO_TRIGGER2,GPIO.OUT)
# input pin: Echo
GPIO.setup(GPIO_ECHO2,GPIO.IN)
# initialize trigger pin to low
GPIO.output(GPIO_TRIGGER2, False)

# define pi GPIO3
GPIO_TRIGGER3 = 20
GPIO_ECHO3    = 21

# output pin: Trigger
GPIO.setup(GPIO_TRIGGER3,GPIO.OUT)
# input pin: Echo
GPIO.setup(GPIO_ECHO3,GPIO.IN)
# initialize trigger pin to low
GPIO.output(GPIO_TRIGGER3, False)


try:
    while True:
        distance1 = measure(GPIO_TRIGGER1, GPIO_ECHO1)
		distance2 = measure(GPIO_TRIGGER2, GPIO_ECHO2)
		#distance3 = measure(GPIO_TRIGGER3, GPIO_ECHO3)
        print("Distance1 : %.1f cm; Distance2 : %.1f cm % (distance1, distance2))
        # send data to the host every 0.5 sec
		
		distance_list = [distance1, distance2]
        client_socket.send(str(distance_list))
        time.sleep(0.2)
finally:
    client_socket.close()
    GPIO.cleanup()	