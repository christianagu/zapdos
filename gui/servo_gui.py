import tkinter as tk
import time
from servo_control.servo import ServoArm



# GUI to control servo. Buttons for each joint and end effector
class ServoGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Servo Controller")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.arm = ServoArm()
        self.counters = {'J': 0, 'B': 0, 'K': 0, 'E': 0}
        self.servo = 'J'

        self.setup_widgets()
        self.update_display()

        self.root.update()  # Update to compute widget sizes
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.root.geometry(f"{width}x{height}")


    # Set up widgets, labels, and grid layout
    def setup_widgets(self):
        """Initialize and configure tkinter widgets."""
        self.servo_a_button = tk.Button(self.root, text="Servo J", command=lambda: self.select_servo('J'))
        self.servo_b_button = tk.Button(self.root, text="Servo B", command=lambda: self.select_servo('B'))
        self.servo_c_button = tk.Button(self.root, text="Servo K", command=lambda: self.select_servo('K'))
        self.servo_d_button = tk.Button(self.root, text="Servo E", command=lambda: self.select_servo('E'))
        self.close_button = tk.Button(self.root, text="Close Arduino", command=self.close_arduino)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_program)
        self.goto_xy_button = tk.Button(self.root, text="Go to (x, y)", command=self.goto_xy)
        self.x_entry = tk.Entry(self.root, width=5)
        self.y_entry = tk.Entry(self.root, width=5)

        self.servo_a_label = tk.Label(self.root)
        self.servo_b_label = tk.Label(self.root)
        self.servo_c_label = tk.Label(self.root)
        self.servo_d_label = tk.Label(self.root)

        self.mButton1 = tk.Button(self.root, text="+10", command=self.increase_by_ten)
        self.mButton2 = tk.Button(self.root, text="-10", command=self.decrease_by_ten)

        self.servo_value_entry = tk.Entry(self.root)
        self.servo_value_entry.insert(0, f"{self.counters[self.servo]}°")

        # Grid configurations
        self.servo_a_button.grid(row=0, column=0, padx=5)
        self.servo_b_button.grid(row=1, column=0, padx=5)
        self.servo_c_button.grid(row=2, column=0, padx=5)
        self.servo_d_button.grid(row=3, column=0, padx=5)

        self.servo_a_label.grid(row=0, column=1, padx=5)
        self.servo_b_label.grid(row=1, column=1, padx=5)
        self.servo_c_label.grid(row=2, column=1, padx=5)
        self.servo_d_label.grid(row=3, column=1, padx=5)
        self.goto_xy_button.grid(row=8, column=0, pady=5)
        self.x_entry.grid(row=8, column=1, pady=5)
        self.y_entry.grid(row=8, column=2, pady=5)

        self.mButton1.grid(row=4, column=0, pady=20, padx=5)
        self.mButton2.grid(row=4, column=1, pady=20, padx=5)
        self.servo_value_entry.grid(row=5, columnspan=2, pady=20)
        self.close_button.grid(row=6, columnspan=2, pady=20)
        self.quit_button.grid(row=7, columnspan=2, pady=20)  # Moved to row=7
        
        self.scan_button = tk.Button(self.root, text="Scan for objects", command=self.scan_for_objects)
        self.scan_button.grid(row=9, columnspan=2, pady=5)
        


    # Function to select our servo
    def select_servo(self, s):
        self.servo = s
        self.update_display()

    def goto_xy(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.arm.set_position(x, y)
        except ValueError:
            print("Invalid x or y input")

    # Function to increase counter
    def increase_by_ten(self):
        if self.counters[self.servo] + 10 <= 180:
            self.counters[self.servo] += 10
            self.arm.move_servo(self.servo, self.counters[self.servo])
        self.update_display()

    # Function to decrease counter
    def decrease_by_ten(self):
        if self.counters[self.servo] - 10 >= 0:
            self.counters[self.servo] -= 10
            self.arm.move_servo(self.servo, self.counters[self.servo])
        self.update_display()
    

    def quit_program(self):
        self.on_closing()  # Close the arduino connection
        self.root.quit()   # End the tkinter mainloop


    # Updates values, buttons, and counter
    def update_display(self):
        # Reset all button colors
        # Reset all button colors
        self.servo_a_button.config(bg="SystemButtonFace")
        self.servo_b_button.config(bg="SystemButtonFace")
        self.servo_c_button.config(bg="SystemButtonFace")
        self.servo_d_button.config(bg="SystemButtonFace")

        # Highlight the selected servo
        if self.servo == 'J':
            self.servo_a_button.config(bg="lightblue")
        elif self.servo == 'B':
            self.servo_b_button.config(bg="lightblue")
        elif self.servo == 'K':
            self.servo_c_button.config(bg="lightblue")
        elif self.servo == 'E':
            self.servo_d_button.config(bg="lightblue")

        self.servo_value_entry.delete(0, tk.END)  # Clear the current text
        self.servo_value_entry.insert(0, f"{self.counters[self.servo]}°")  # Insert the new value
        self.servo_a_label.config(text=f"Servo J: {self.counters['J']}°")
        self.servo_b_label.config(text=f"Servo B: {self.counters['B']}°")
        self.servo_c_label.config(text=f"Servo K: {self.counters['K']}°")
        self.servo_d_label.config(text=f"Servo E: {self.counters['E']}°")


    # Close our arduino connection
    def close_arduino(self):
        self.arm.close()
    def on_closing(self):
        self.close_arduino()


    # event for if our value is changed
    def on_value_changed(self,event):
        try:
            # Extract number from the entry (without the degree symbol)
            value = int(self.servo_value_entry.get().replace('°', ''))
            if 0 <= value <= 180:
                self.counters[self.servo] = value
            else:
                raise ValueError
        except ValueError:  # If input is not valid, reset to the current value of the servo
            self.counters[self.servo] = self.counters.get(self.servo, 0)  # Fetch current value or default to 0
        self.update_display()

   # (ServoGUI class continued...)

    def scan_for_objects(self):
        for pos in range(0, 181, 45):  # Scans from 0 to 180 degrees in steps of 45
            self.arm.move_servo('J', pos)  # rotate the base
            time.sleep(1)  # give some time to stabilize
            distance = self.arm.read_distance()
            if distance and distance < 50:  # Set a threshold for detection
                print(f"Object detected at {pos} degrees and distance {distance} cm")
                # Now use the set_position method to orient the arm to this position
                self.arm.set_position(distance, 0)  # 0 for y as we're assuming 2D plane
                break



if __name__ == "__main__":
    root = tk.Tk()
    app = ServoGUI(root)
    root.mainloop()