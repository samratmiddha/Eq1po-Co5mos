import os
import pyautogui
import time
import ast

from alias import alias as alias_function
from set_alias import set_alias

def list_files_in_logs_folder():
    logs_folder = "Logs"
    files = os.listdir(logs_folder)
    return files

def select_file(files):
    print("Choose a file to process:")
    for index, file in enumerate(files):
        print(f"{index + 1}. {file}")

    while True:
        try:
            choice = int(input("Enter the number of the file you want to process: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():

    TIME_INTERVAL = 1
    PIXELS_PER_CLICK = 0.8


    files = list_files_in_logs_folder()
    if not files:
        print("No files found in Logs folder.")
        return

    selected_file = select_file(files)
    file_path = os.path.join("Logs", selected_file)
    print(f"Selected file: {file_path}")

    while True:

        # Open the file
        with open(file_path, 'r') as file:
            # Read the lines
            lines = file.readlines()

            print(lines)

            if (lines[-1].split(';')[0].find('.') != -1):
                print("No alias found. Creating alias...")
                alias_function(file_path)


                with open(file_path, 'r') as file:
                    lines = file.readlines()
                print(lines)


            alias = ast.literal_eval(lines[-1].split(';')[1].strip())

            # for i in range(len(alias)):

            for sublist in alias:

                print(lines)
                index = sublist[0]
                value = sublist[1]

                parts = lines[index].split(';')
                parts[1] = value
                lines[index] = ';'.join(parts)



            alias_values = set_alias(file_path)

            for sublist in alias:
                index = sublist[0]

                value = alias_values[str(index)][1]
                parts = lines[index].split(';')
                parts[1] = value
                lines[index] = ';'.join(parts)



            start_time = 0
            # Process each line
            for line in lines[:-1]:
                print(line)
                parts = line.split(';')
                timestamp_parts = parts[0].split(':')
                timestamp = float(timestamp_parts[0])*3600 + float(timestamp_parts[1])*60 + float(timestamp_parts[2])
                action = parts[2].strip()
                keystrokes = parts[1].strip()

                print(action, keystrokes, "ACTION")

                if len(keystrokes) != 0:
                    print(f'time interval: {(timestamp-start_time)/len(keystrokes)}')
                    pyautogui.write(keystrokes, interval=((timestamp-start_time)/len(keystrokes)))

                    if action.split('.')[0] == 'Key':
                        pyautogui.press(action.split('.')[1], interval=(timestamp-start_time)/len(keystrokes))

                elif action.split('.')[0] == 'Key':



                    if '+' in action:
                        key1 = action.split('+')[0].split('.')[1].strip()
                        key2 = action.split('+')[1].split('.')[1] if '.' in action.split('+')[1] else action.split('+')[1].strip()

                        print(key1, key2, "KEYS")
                        pyautogui.hotkey(key1, key2)

                    else:

                        pyautogui.press(action.split('.')[1], interval=(timestamp-start_time))

                elif action.split(' ')[0] == 'mouse' and action.split(' ')[1] == 'scrolled':
                    x, y = action.split(' ')[-5:-3]
                    dx, dy = action.split(' ')[-2:]
                    # Convert from clicks to pixels
                    dx_pixels = int(float(dx)) * PIXELS_PER_CLICK
                    dy_pixels = int(float(dy)) * PIXELS_PER_CLICK
                    # Scroll
                    # time.sleep(timestamp - start_time)  # Add this line to introduce an interval
                    pyautogui.moveTo(int(float(x)), int(float(y)))  # Move to the correct location
                    pyautogui.scroll(dy_pixels)  # Scroll vertically
                    pyautogui.hscroll(dx_pixels)  # Scroll horizontally
                    print(x, y, dx_pixels, dy_pixels)

                elif action.split(' ')[0] == 'mouse' and action.split(' ')[1] == 'clicked':
                    print(action)
                    x_cord, y_cord = action.split(' ')[-4:-2]
                    print(x_cord, y_cord)
                    button_type = action.split(' ')[-1].split('.')[1]
                    print(button_type)
                    pyautogui.click(button=button_type, x = int(float(x_cord)), y = int(float(y_cord)), interval=(timestamp-start_time))

                elif action.split(' ')[0] == 'end':
                    break

                print(timestamp)

                start_time = timestamp

            user_input = input("Do you want to process the file again? (Press Enter to continue, or type 'exit' to exit): ")
            if user_input.lower() == "exit":
                break


if __name__ == "__main__":
    main()
