import os
import random
import sqlite3
import string
import tkinter as tk

import cv2
from PIL import Image, ImageTk

# Create a connection to the SQLite database
conn = sqlite3.connect('attendance.db')

# Create a table named 'image_labels' in the database if it doesn't exist
conn.execute('''CREATE TABLE IF NOT EXISTS image_labels
                 (image_name TEXT PRIMARY KEY, usn TEXT,name TEXT)''')

def capture():
    img_counter = 0
    cam = cv2.VideoCapture(0)
    usn = ""
    name=""

    def capture_frame():
        nonlocal img_counter
        nonlocal usn
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            return
        if os.path.exists('my_db/representations_facenet.pkl'):
            os.remove('my_db/representations_facenet.pkl')

        # Generate a random image name
        image_name = usn+generate_random_name() + ".png"
        cv2.imwrite(os.path.join("my_db", image_name), frame)
        print("Image captured:", image_name)
        img_path="my_db/"+image_name

        # Store the image name and USN in the database
        conn.execute("INSERT INTO image_labels (image_name, usn,name) VALUES (?, ?, ?)", (img_path, usn,name))
        conn.commit()

        img_counter += 1



    def quit_app():
        
        cam.release()
        conn.close()
        root.destroy()

    def set_usn():
        nonlocal usn
        nonlocal name
        name=entry_name.get()
        usn = entry_usn.get()
        usn=usn.upper()
        print("USN:", usn)
        print("Name: ",name)

    def generate_random_name():
        random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return random_name
    

    root = tk.Tk()
    root.title("Enroll your face")

    usn_label = tk.Label(root, text="usn")
    usn_label.pack()

    entry_usn = tk.Entry(root)
    entry_usn.pack(pady=10)

    name_label=tk.Label(root,text="Name")
    name_label.pack()

    entry_name = tk.Entry(root)
    entry_name.pack(pady=10)

    btn_set_usn = tk.Button(root, text="Set Details", command=set_usn)
    btn_set_usn.pack(pady=5)

    btn_capture = tk.Button(root, text="Capture Frame", command=capture_frame)
    btn_capture.pack(pady=10)

    btn_quit = tk.Button(root, text="Quit", command=quit_app)
    btn_quit.pack(pady=10)

    os.makedirs("my_db", exist_ok=True)

    def process_frame():
        ret, frame = cam.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            img = img.resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)
            label_preview.imgtk = imgtk
            label_preview.configure(image=imgtk)
        label_preview.after(10, process_frame)

    label_preview = tk.Label(root)
    label_preview.pack(padx=10, pady=10)

    root.protocol("WM_DELETE_WINDOW", quit_app)
    process_frame()
    root.mainloop()


capture()
