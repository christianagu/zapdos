from gui.servo_gui import ServoGUI  # Assuming you have a function in servo_gui.py to run the GUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = ServoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()