import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os
import cv2
import time

def launch_game(game_script):
    if os.path.exists(game_script + '.py'):
        game_script += '.py'
    else:
        game_script += '.pyc'
    subprocess.Popen(["python", game_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def update_contrast(value):
    with open('config.txt', 'r') as config_file:
        lines = config_file.readlines()

    for i, line in enumerate(lines):
        if line.startswith('CONTRAST='):
            lines[i] = f'CONTRAST={value}\n'

    with open('config.txt', 'w') as config_file:
        config_file.writelines(lines)

def start_recording():
    global recording, selected_camera
    recording = True
    selected_camera_name = camera_var.get()  # Get the selected camera source name
    selected_camera = available_cameras.index(selected_camera_name)  # Convert to camera index
    threading.Thread(target=record_camera).start()  # Start recording in a separate thread

def stop_recording():
    global recording
    recording = False

def record_camera():
    global recording, selected_camera
    # Create the "response" folder if it doesn't exist
    recording_folder = "recording"
    os.makedirs(recording_folder, exist_ok=True)
    # Generate a unique filename based on the current time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    video_filename = f"{recording_folder}/recording_{timestamp}.avi"

    cap = cv2.VideoCapture(selected_camera)
    if not cap.isOpened():
        print("Error opening camera")
        return
    width, height = int(cap.get(3)), int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))

    while recording:
        ret, frame = cap.read()
        if not ret:
            break  # Break out of the loop if camera capture fails
        out.write(frame)

        # Show the frame in a separate window
        cv2.imshow('Camera Recording', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def get_available_cameras():
    available_cameras = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        camera_name = f"Camera {index}"
        available_cameras.append(camera_name)
        cap.release()
        index += 1
    return available_cameras

def main_menu():
    global camera_var, available_cameras  # Declare camera_var as a global variable

    root = tk.Tk()
    root.title("Optometry Games Menu")
    root.geometry("400x600")

    label = tk.Label(root, text="Optometry Games Menu", font=("Helvetica", 20))
    label.pack(pady=20)

    # Read the initial contrast value from config.txt
    default_contrast = read_initial_contrast()

    # Add a slider to adjust contrast
    slider_label_text = "Adjust Contrast (0-10):"
    slider_label = tk.Label(root, text=slider_label_text, font=("Helvetica", 12))
    slider_label.pack()
    contrast_slider = tk.Scale(root, from_=0, to=10, orient="horizontal", length=300, showvalue=True, command=update_contrast)
    contrast_slider.set(default_contrast)  # Set the default value
    contrast_slider.pack()

    # Add a note about contrast change
    note_label = tk.Label(root, text="* Changes take effect on game restart", font=("Helvetica", 10), fg="gray")
    note_label.pack()

    # Add a button to launch game1.py
    button1 = tk.Button(root, text="Visual Reaction Time", command=lambda: launch_game("game1"), font=("Helvetica", 12))
    button1.pack(pady=20)

    # Add a button to launch game2.py
    button2 = tk.Button(root, text="Distance vs Near Target", command=lambda: launch_game("game2"), font=("Helvetica", 12))
    button2.pack(pady=(0,20))

    # Add a button to launch game3.py
    button3 = tk.Button(root, text="Length of time required", command=lambda: launch_game("game3"), font=("Helvetica", 12))
    button3.pack(pady=(0,20))

    # Add a separator to visually separate sections
    separator = ttk.Separator(root, orient="horizontal")
    separator.pack(fill="x", pady=20)

    # Add camera recording section (You will need to implement this part)
    camera_label = tk.Label(root, text="Camera Recording", font=("Helvetica", 16))
    camera_label.pack()

    # Dropdown menu to select camera source
    camera_label = tk.Label(root, text="Select Camera Source:", font=("Helvetica", 12))
    camera_label.pack()
    available_cameras = get_available_cameras()  # Get available camera sources
    camera_var = tk.StringVar(value=available_cameras[0])  # Set default to the first available camera
    camera_dropdown = ttk.Combobox(root, textvariable=camera_var, values=available_cameras)
    camera_dropdown.pack()

    # Add buttons for recording
    recording_buttons_frame = tk.Frame(root, pady=20)  # Add padding/margin from above
    start_button = tk.Button(recording_buttons_frame, text="Start Recording", command=start_recording, font=("Helvetica", 12))
    start_button.pack(side=tk.LEFT, padx=10)
    stop_button = tk.Button(recording_buttons_frame, text="Stop Recording", command=stop_recording, font=("Helvetica", 12))
    stop_button.pack(side=tk.LEFT, padx=10)
    recording_buttons_frame.pack()

    root.mainloop()

def read_initial_contrast():
    if os.path.exists('config.txt'):
        with open('config.txt', 'r') as config_file:
            lines = config_file.readlines()
            for line in lines:
                if line.startswith('CONTRAST='):
                    try:
                        return int(line.split('=')[1])
                    except (ValueError, IndexError):
                        pass
    return 0  # Default contrast value if file doesn't exist or value is invalid

if __name__ == "__main__":
    recording = False  # Global variable to track recording state
    selected_camera = 0  # Default camera source
    main_menu()
