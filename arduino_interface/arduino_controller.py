import serial
import time

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

    def close(self):
        if self.connection and self.connection.is_open:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Failed to close Arduino connection. Error: {e}")
