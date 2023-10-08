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


"""
class ArduinoController:
    def __init__(self, port='COM5', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  # give the connection a second to establish
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino on port {self.port}. Error: {e}")

    def send_command(self, command):
        if self.connection and self.connection.is_open:
            try:
                self.connection.write(command.encode())
            except Exception as e:
                print(f"Failed to send command {command}. Error: {e}")
        else:
            print("Arduino connection is not open.")
    
    def read_line(self):
        return self.connection.readline().decode('utf-8').strip() if self.connection else None

    def close(self):
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Failed to close Arduino connection. Error: {e}")

"""
