import serial
import time
import RPi.GPIO as GPIO

class RaspberryPiController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
    
    def setup_servo(self, pin):
        GPIO.setup(pin, GPIO.out)
        return GPIO.pwn(pin, 50) # set frequency to 50hz
    
    def set_servo_angle(self, servo, angle):
        duty_cycle = (angle / 18) + 2 # Convert angle to duty cycle
        servo.start(duty_cycle)
        time.sleep(0.5)
        servo.stop()

    def cleanup(self):
        GPIO.cleanup()