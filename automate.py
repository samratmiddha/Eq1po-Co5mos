import pyautogui
import time
import os
import sys

# Ask for the log file
log_file = input("Enter the name of the log file: ")
file_path = f'./Logs/{log_file}'

# Open the file
if not os.path.exists(file_path):
    print(f"The given file {file_path} does not exist")
    sys.exit(1)

else:
    with open(file_path, 'r') as file:
        # Read the lines
        lines = file.readlines()

        start_time = 0

    # Process each line
    for line in lines:
        parts = line.split(';')
        timestamp_parts = parts[0].split(':')
        timestamp = float(timestamp_parts[0])*3600 + float(timestamp_parts[1])*60 + float(timestamp_parts[2])
        action = parts[2].strip()
        keystrokes = parts[1].strip()

        print(action, keystrokes)

        if len(keystrokes) != 0:
            pyautogui.write(keystrokes, interval=(timestamp-start_time)/len(keystrokes))

            if action.split('.')[0] == 'Key':
                pyautogui.press(action.split('.')[1], interval=timestamp-start_time/len(keystrokes))

        elif action.split('.')[0] == 'Key':
            pyautogui.press(action.split('.')[1], interval=timestamp-start_time)


        elif action.split(' ')[0] == 'mouse' and action.split(' ')[1] == 'scrolled':
            x, y = action.split(' ')[-5:-3]
            dx, dy = action.split(' ')[-2:]
            # pyautogui.scroll(int(dy), x=int(x), y=int(y))
            print(x, y, dx, dy)

            # pyautogui.moveTo(int(float(x)), int(float(y)))
            pyautogui.vscroll(dx)
            time.sleep(0.1)
            pyautogui.hscroll(dy)

        elif action.split(' ')[0] == 'mouse' and action.split(' ')[1] == 'clicked':
            x, y = action.split(' ')[-2:]
            pyautogui.click(int(float(x)), int(float(y)), interval=timestamp-start_time)

        elif action.split(' ')[0] == 'end':
            break

        print(timestamp)

        start_time = timestamp
