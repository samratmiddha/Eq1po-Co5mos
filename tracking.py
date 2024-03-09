import datetime
import os
from pynput import keyboard, mouse

# Get the current date and time
current_datetime = datetime.datetime.now()

# Format the date and time as a string
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Specify the folder path where you want to store the file
folder_path = "/home/psyduck/Desktop/Log_File"

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)

# Create the full file path including folder path and filename
filename = os.path.join(folder_path, f"{formatted_datetime}.txt")

# Global variables
logged_string = ""
escape_pressed = False
current_keys = set()  # To track currently pressed keys
start_date_time = datetime.datetime.now()

# Function to write the logged keys to a file
def write_to_file(string):
    current_time = datetime.datetime.now()
    with open(filename, "a") as f:
        f.write(f"{current_time - start_date_time} ; {string}\n")

def on_press(key):
    global escape_pressed, logged_string, current_keys
    try:
        if key == keyboard.Key.esc:
            escape_pressed = True
            # Log any pending input before exiting.
            if logged_string or current_keys:
                log_keys("Line Break: Escape Key")
            return False
        elif key in [keyboard.Key.space, keyboard.Key.enter]:
            # Identify the line breaker key
            line_breaker = "Space" if key == keyboard.Key.space else "Enter"
            # Log as a line break if there's input; reset afterwards.
            if logged_string or current_keys:
                log_keys(f"Line Break: {line_breaker} Key")
            logged_string = ""  # Prepare for new input.
        else:
            if hasattr(key, 'char'):
                # Regular character keys are treated differently based on current state.
                if current_keys:
                    # If modifier keys are held, log each press with them.
                    logged_string = key.char
                    log_keys()
                else:
                    # Accumulate characters if no modifier is held.
                    logged_string += key.char
            else:
                # For non-character keys (modifiers included), log immediately if there's existing input.
                if logged_string or (key not in current_keys and current_keys):
                    current_keys.add(key)
                    log_keys()
                else:
                    # Simply add modifier keys to the set if no prior input exists.
                    current_keys.add(key)
    except Exception as e:
        print(f"Error in on_press: {e}")

def log_keys(message=""):
    global current_keys, logged_string
    # Prepare the combination or single keys for logging
    combo = ' + '.join([key.name for key in current_keys] + [logged_string.strip()]) if current_keys else logged_string
    # Add the optional message if provided (for line breakers)
    combo = f"{combo}; {message}" if message else combo
    if combo.strip():  # Ensure there's content to log
        write_to_file(combo)


def on_release(key):
    global current_keys
    if key in current_keys:
        current_keys.remove(key)

def on_click(x, y, button, pressed):
    global escape_pressed
    if pressed:
        log_keys()  # Log any keys before the click event
        write_to_file('" ";'f"Mouse clicked at {x}, {y} with {button}")
    if escape_pressed:
        
        return False

def on_scroll(x, y, dx, dy):
    log_keys()  # Log any keys before the scroll event
    write_to_file(f"Mouse scrolled at {x}, {y} by {dx}, {dy}")
    if escape_pressed:
        return False

# Start keyboard listener in a separate thread
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# Start mouse listener in a separate thread
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

# Join both threads
keyboard_listener.join()
mouse_listener.join()

