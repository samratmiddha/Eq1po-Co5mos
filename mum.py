import datetime
import os

# Get the current date and time
current_datetime = datetime.datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Specify the folder path where you want to store the file
folder_path = "/home/psyduck/Desktop/Log_File"

# Create the full file path including folder path and filename
filename = os.path.join(folder_path, f"{formatted_datetime}.txt")

from pynput import keyboard
from pynput import mouse
import datetime


# Global variable to store the logged keys
logged_string=""
escape_pressed = False

start_date_time = datetime.datetime.now()

# Function to write the logged keys to a file
def write_to_file(string):
    global start_date_time
    current_time = datetime.datetime.now()
    with open(filename, "a") as f:
            f.write(str(current_time-start_date_time)+" ; "+string+"\n")

# Function to handle key press events
def on_press(key):
    global logged_string,escape_pressed
    try:
        logged_string+=key.char
        
    except AttributeError:
        write_to_file(logged_string +" ; " +str(key))
        logged_string=""
    if key ==keyboard.Key.esc:
        escape_pressed =True

# Function to handle key release events
def on_release(key):
    global logged_string,escape_pressed
    if escape_pressed:
        write_to_file(logged_string + ";"+"end")
        logged_string=""
        return False
        


def on_click(x, y, button, pressed):
    global logged_string,escape_pressed
    write_to_file(logged_string +" ; " +f"mouse clicked at {x} {y}")
    logged_string=""
    if escape_pressed:
        return False
    
def on_scroll(x, y, dx, dy):
    global logged_string,escape_pressed
    write_to_file(logged_string +" ; " +f"mouse scrolled at {x} {y} by {dx} {dy} ")
    logged_string=""
    if escape_pressed:
        return False
    

    
# Start keyboard listener in a separate thread
keyboard_listener =keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

# Start mouse listener in a separate thread
mouse_listener = mouse.Listener(
    on_click=on_click,
    on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

# Join both threads
keyboard_listener.join()
mouse_listener.join()