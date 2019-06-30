import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish
from range import RangeSensor

MQTT_SERVER = "192.168.1.90"
MQTT_PATH = "/home/basement/sump/waterlevel"

TRIG = 17
ECHO = 27

try:
    GPIO.setmode(GPIO.BCM)
    #GPIO.setmode(GPIO.BOARD)

    rs = RangeSensor(ECHO, TRIG)
    distanceMeters = rs.measureSingleDistance()
    distanceCM = round(distanceMeters*100, 2)
    
    publish.single(MQTT_PATH, str(distanceCM), hostname=MQTT_SERVER)
finally:
    GPIO.cleanup()