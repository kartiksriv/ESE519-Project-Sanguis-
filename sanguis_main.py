# Project : SANGUIS
# This code extracts the dyed patch from the image and then finds the mean of V in the HSV range
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import picamera
import datetime
from time import gmtime, strftime, sleep
import paho.mqtt.client as paho

broker="iot.eclipse.org"
port = 1883
client= paho.Client("client-001")
camera= picamera.PiCamera()

#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.payload.decode("utf-8")))

def imgprocess():
    time.sleep(1)
    camera.capture('/home/pi/Desktop/Sample.png');
    img0 = cv2.imread('/home/pi/Desktop/Sample.png')
    img1 = cv2.cvtColor(img0,cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img0,cv2.COLOR_BGR2HSV)
    img3 = cv2.cvtColor(img0,cv2.COLOR_BGR2HLS)
    # Defining a range of HSV vlaues to extract the region of interest
    lower_blue = np.array([80,60,0])
    upper_blue = np.array([125,255,255])
    # Thresholding the original image within the defined range
    mask = cv2.inRange(img2, lower_blue, upper_blue)
    # Masking the original image
    res = cv2.bitwise_and(img3,img3, mask= mask)
    #Calculating the mean of value
    v_mean = cv2.mean(res[:,:,1], mask=mask)
    cv2.imshow('res', res)
    return v_mean[0]
    

def push_to_broker(result):
    print (result)
    f = open("/home/pi/Desktop/Sample_Values.txt","a")
    f.write('{}\n'.format(result))
    f.close()

    f = open("/home/pi/Desktop/Sample_Values.txt","r+")
    lines = f.readlines()
    for line in lines:
        print("publishing ")
        client.publish("Sanguis/count",line)#publish
        time.sleep(1)
    client.publish("Sanguis/count",str(result))#publish
    f.close()

def SetAngle(pwm, angle):
    duty = angle/18 +2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)
    
def pull_action():
    pwm = GPIO.PWM(3, 50)
    pwm.start(0)
    
    SetAngle(pwm, 0)
    pwm.stop()

def push_action():
    pwm = GPIO.PWM(3, 50)
    pwm.start(0)
    
    SetAngle(pwm, 180)
    pwm.stop()
    
def start_process():

    #Bind function to callback
    client.on_message=on_message
    print("connecting to broker ",broker)
    client.connect(broker, port)#connect
    client.loop_start() #start loop to process received messages
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    #syringe injection
    GPIO.setup(3, GPIO.OUT)
    pull_action()

    GPIO.setup(8,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(10,GPIO.OUT,initial=GPIO.LOW)
    GPIO.output(8,GPIO.HIGH)
    GPIO.output(10,GPIO.HIGH)
    
    #camera.start_preview()
    
    start= time.time()
    time.clock()
    elapsed = 0
    result = imgprocess()
    
    push_action()
    GPIO.output(8,GPIO.LOW)
    GPIO.output(10,GPIO.LOW)

    push_to_broker(result)
    client.disconnect() #disconnect
    client.loop_stop() #stop loop
    
def main():
    start_process()
    
if __name__=="__main__":
    main()
