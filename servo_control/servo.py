import time
from arduino_interface.arduino_controller import ArduinoController


class ServoArm:
    
    def __init__(self, arduino_port='COM5'):
        self.arduino = ArduinoController(port=arduino_port)
        self.arduino.connect()
        self.pos_array = [0, 45, 90, 135, 180]

    def move_servo(self, servo_id, position):
        command = servo_id + str(position) + "\n"
        self.arduino.send_command(command)
        print(f"Sending command: {command}")
        time.sleep(0.5)  # give the servo time to reach the position


    # Digital Pin 2
    def endeffector(self):
        endeffector_flag = True # This should likely be determined some other way, for now it's always True
        if endeffector_flag:
            print("endeffector = true")
            self.move_servo('E', self.pos_array[-1])
        else:
            print("endeffector = false")
            self.move_servo('E', self.pos_array[-1])

    # Digital Pin 5
    def lower_link_joint(self):
        lower_link_joint = True
        if lower_link_joint:
            print("lower_link_joint = true")
            self.move_servo('K', self.pos_array[-1])
        else:
            print("lower_link_joint = false")
            self.move_servo('K', self.pos_array[-1])

    # Digital Pin 4
    def upper_link_joint(self):
        upper_link_joint = True
        if upper_link_joint:
            print("upper_link_joint = true")
            self.move_servo('B', self.pos_array[-1])
        else:
            print("upper_link_joint = false")
            self.move_servo('B', self.pos_array[-1])

    # Digital Pin 3
    def base_rotation_joint(self):
        base_rotation_joint = True
        if base_rotation_joint:
            print("base_rotation_joint = true")
            self.move_servo('J', self.pos_array[0])
        else:
            print("base_rotation_joint = false")
            self.move_servo('J', self.pos_array[-1])
    
    def close(self):
        self.arduino.close()
