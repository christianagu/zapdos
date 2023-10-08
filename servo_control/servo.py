import time
import math
from arduino_interface.arduino_controller import ArduinoController
from arduino_interface.raspberry_pi_controller import RaspberryPiController

class ServoArm:
    
    L1 = 80
    L2 = 150

    servo_pin_mapping = {
        'J': 17,  # Base
        'B': 4,   # Upper Link
        'K': 3,   # Lower Link
        'E': 2    # End Effector
    }

    def __init__(self):
        self.pi_controller = RaspberryPiController()
        self.servos = {key: self.pi_controller.setup_servo(val) for key, val in self.servo_pin_mapping.items()}

    def move_servo(self, servo_id, position):
        if servo_id in self.servos:
            self.pi_controller.set_servo_angle(self.servos[servo_id], position)
        else:
            print(f"Unknown servo_id: {servo_id}")

    def set_position(self, x, y):
        r = math.sqrt(x**2 + y**2)
        computed_value = (r**2 + self.L1**2 - self.L2**2) / (2 * self.L1 * r)
        computed_value = max(-1, min(computed_value, 1))
        if computed_value < -1 or computed_value > 1:
            # Handle the error or adjust the value
            # For example, you might cap the values at -1 or 1
            computed_value = max(-1, min(computed_value, 1))
        alpha = math.acos(computed_value)



        alpha = math.acos((r**2 + self.L1**2 - self.L2**2) / (2 * self.L1 * r))
        beta = math.atan2(y, x)
        gamma = math.acos((self.L1**2 + self.L2**2 - r**2) / (2 * self.L1 * self.L2))
        
        theta1 = beta + alpha # + is the correct config
        theta2 = math.pi - gamma
        
        # Convert angles from radians to degrees
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)
        
        # Send commands to move the servos (assuming 'B' is the first joint and 'K' is the second)
        self.move_servo('B', theta1_deg)
        self.move_servo('K', theta2_deg)

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
    
    def read_distance(self):
        line = self.arduino.read_line()
        if "Distance:" in line:
            distance = int(line.split(":")[1].strip())
            return distance
        return None

    def close(self):
        self.pi_controller.cleanup()


"""
class ServoArm:
    
    L1 = 80
    L2 = 150

    def __init__(self, arduino_port='COM5'):
        self.arduino = ArduinoController(port=arduino_port)
        self.arduino.connect()
        self.pos_array = [0, 45, 90, 135, 180]

    def move_servo(self, servo_id, position):
        command = servo_id + str(position) + "\n"
        self.arduino.send_command(command)
        print(f"Sending command: {command}")
        time.sleep(0.5)  # give the servo time to reach the position

    def set_position(self, x, y):
        r = math.sqrt(x**2 + y**2)
        computed_value = (r**2 + self.L1**2 - self.L2**2) / (2 * self.L1 * r)
        computed_value = max(-1, min(computed_value, 1))
        if computed_value < -1 or computed_value > 1:
            # Handle the error or adjust the value
            # For example, you might cap the values at -1 or 1
            computed_value = max(-1, min(computed_value, 1))
        alpha = math.acos(computed_value)



        alpha = math.acos((r**2 + self.L1**2 - self.L2**2) / (2 * self.L1 * r))
        beta = math.atan2(y, x)
        gamma = math.acos((self.L1**2 + self.L2**2 - r**2) / (2 * self.L1 * self.L2))
        
        theta1 = beta + alpha # + is the correct config
        theta2 = math.pi - gamma
        
        # Convert angles from radians to degrees
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)
        
        # Send commands to move the servos (assuming 'B' is the first joint and 'K' is the second)
        self.move_servo('B', theta1_deg)
        self.move_servo('K', theta2_deg)

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
    
    def read_distance(self):
        line = self.arduino.read_line()
        if "Distance:" in line:
            distance = int(line.split(":")[1].strip())
            return distance
        return None

    def close(self):
        self.arduino.close()
"""