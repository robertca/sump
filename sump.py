import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish
from range import RangeSensor

MQTT_SERVER = "192.168.1.90"
MQTT_PATH = "/home/basement/sump/waterlevel"

TRIG = 17
ECHO = 27

# Distance in CM that the sensor is from the ground
HEIGHT_GROUND = 105.0

try:
    GPIO.setmode(GPIO.BCM)

    # Calculate the measured distance in CM
    rs = RangeSensor(ECHO, TRIG)
    distanceMeters = rs.measureAverage(2, 2)
    distanceCM = distanceMeters * 100

    # Work out amount of water
    waterHeightCM = HEIGHT_GROUND - distanceCM
    waterHeightCM = round(waterHeightCM, 2)

    waterHeightCM = max(0.0, waterHeightCM)

    publish.single(MQTT_PATH, str(waterHeightCM), hostname=MQTT_SERVER)
except Exception as e:
    print(e)
finally:
    GPIO.cleanup()
