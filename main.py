#Libraries
import RPi.GPIO as GPIO
import time
from gpiozero import AngularServo


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23 
GPIO_ECHO =  24

GPIO_TRIGGER_SENS2 = 25
GPIO_ECHO_SENS2 = 8
LED_OUT = 7

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_SENS2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_SENS2, GPIO.IN)

GPIO.setup(LED_OUT, GPIO.OUT)

# setup to send a text notification
username = 'sdoru2@illinois.edu' # Your ClickSend username 
api_key = '694445E4-572A-DDF9-6F6C-7CE073AD7F2B'

msg_to = '+13194916766' # Recipient Mobile Number in international format (+61411111111 test number). 
msg_from = '' # Custom sender ID (leave blank to accept replies). 
msg_body = 'Hello, This is notification from Smart Trash Bin - Bin is close to full!!' # The message to be sent. 

import json, subprocess 



def motion_sens_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
def distance_bin_level():
    # set TRIGGER_SENS2 to HIGH
    GPIO.output(GPIO_TRIGGER_SENS2, True)
 
    # set TRIGGER_SENS2 after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_SENS2, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_SENS2) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_SENS2) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance
    
def openTrashLid():
    servo.angle = 90
    time.sleep(3)
    servo.angle = -40
    return
 
if __name__ == '__main__':
    servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023, initial_angle=-40)
    servo.angle = -40
    GPIO.output(LED_OUT, False)
    notification_sent = False 
    bin_full_counter = 0
    while True:
        dist = motion_sens_distance()
        #print(dist)
        time.sleep(0.005)
        if dist <= 40:
            openTrashLid()
        
        bin_level_dist = distance_bin_level()
        # to avoid glitch, make sure bin low is detected at-leasr few times before sending a notification
        if bin_level_dist < 10:
          bin_full_counter = bin_full_counter + 1

        if bin_full_counter >= 10:
            if not notification_sent:
                print ("measured bin distance level", bin_level_dist)
                #send a text notification
                request = { "messages" : [ { "source":"rpi", "from":msg_from, "to":msg_to, "body":msg_body } ] } 
                request = json.dumps(request) 

                cmd = "curl https://rest.clicksend.com/v3/sms/send -u " + username + ":" + api_key + " -H \"Content-Type: application/json\" -X POST --data-raw '" + request + "'" 
                p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

                (output,err) = p.communicate()
                notification_sent = True
            GPIO.output(LED_OUT, True)
        
        #When bin is emptied reset the LED and notification flag 
        if bin_level_dist > 25: 
          GPIO.output(LED_OUT, False)
          notification_sent = False
          bin_full_counter = 0
            


