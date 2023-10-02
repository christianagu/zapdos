import serial
import time

# Establish connection to the Arduino
arduino = serial.Serial('COM5', 9600)
time.sleep(2)  # give the connection a second to establish



class servo_arm:

    def move_servo(position):
        command = str(position) + "\n"  # Add a newline character at the end
        arduino.write(command.encode())  # send the position to the Arduino
        time.sleep(0.5)  # give the servo time to reach the position


    pos_array = [0, 45, 90, 135, 180]

    def endeffector(pos_array):
        endeffector_flag = True # If obj is detected, endeffector = true
        if endeffector_flag == True:
            print("endeffector = true")
            move_servo(pos_array[0])
        else:
            print("endeffector = false")
            move_servo(pos_array[-1])



endeffector(pos_array)



arduino.close()  # close the connection
