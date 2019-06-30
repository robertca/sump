import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

# https://www.linuxnorth.org/raspi-sump/HC-SR04Users_Manual.pdf

class RangeSensor:
    def __init__(self, gpioEcho, gpioTrig):
        self.GPIO_ECHO = gpioEcho
        self.GPIO_TRIG = gpioTrig
        self.sensorTrigger = 1e-6

        self.conversion = 346.0 # 346m/s - speed of sound

        # Set up the Input and Output Pins
        GPIO.setup(self.GPIO_TRIG, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    # Runs a single range measurement
    # Returns: Distance in meters, or None if an error occurred
    def measureSingleDistance(self):
        GPIO.output(self.GPIO_TRIG, False)
        time.sleep(0.5)

        # Trigger the Pulse Wave
        GPIO.output(self.GPIO_TRIG, True)
        time.sleep(self.sensorTrigger)
        GPIO.output(self.GPIO_TRIG, False)

        # We'll be receiving Low (0) while the sensor is transmitting
        run_time = time.time() + 4 # seconds
        start_time = None
        end_time = None

        while time.time() < run_time:
            if GPIO.input(self.GPIO_ECHO):
                start_time = time.time()
                break

        while time.time() < run_time:
            if not GPIO.input(self.GPIO_ECHO):
                end_time = time.time()
                break
            
        # Something went wrong and we didn't get any valid measurements
        if start_time == None or end_time == None or end_time <= start_time:
            return None
        
        time_diff = end_time - start_time
        return self.conversion * (time_diff / 2.0)

    # Returns: Distance in meters
    def measureAverage(self, runs = 1, wait = 2):
        totalDistance = 0
        successRuns = 0.001

        for i in range(0, max(0, runs)):
            distance = self.measureSingleDistance()
            if distance != None:
                totalDistance += distance
                successRuns += 1
            
            time.sleep(wait)

        return totalDistance / successRuns
