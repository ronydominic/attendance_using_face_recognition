import datetime
import os
import sqlite3
import threading
import time
import tkinter as tk

import cv2
from deepface import DeepFace
from PIL import Image, ImageTk

image = Image.new('RGB', (640,480), color='white')
image.save('white_image.png')
try:
    DeepFace.find(img_path='white_image.png',db_path="my_db",model_name="Facenet")
except:
    pass    

if not os.path.exists("tmp_folder"):
    os.makedirs("tmp_folder")

# Variable to store the starting time
starting_time = time.time()

# List to store the running state of thread_1
thread_1_running = [False]

def process_images():
    global starting_time
    # Get the list of image files in the tmp_folder
    starting_time = time.time()
    image_files = os.listdir("tmp_folder")
    for image_file in image_files:
        image_path = os.path.join("tmp_folder", image_file)
        try:
            result = DeepFace.find(img_path=image_path, db_path="my_db", enforce_detection=True, model_name="Facenet")

            if result[0].empty:
                pt = ""
            else:
                pt = result[0].identity[0]
            if pt != "":
                print("hi")
            print(pt)
            # Remove the processed image file
            ####modification starts
            # Connect to the SQLite database
            conn = sqlite3.connect("attendance.db")
            cursor = conn.cursor()

            # Retrieve the USN value for the matching image_name
            cursor.execute("SELECT usn,name FROM image_labels WHERE image_name = ?", (pt,))
            usn_result = cursor.fetchone()

            if usn_result is not None:
                usn1 = usn_result[0]
                name1=usn_result[1]
                print("USN:", usn1)
                print("name: ",name1)
                ###mod1
                cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    usn TEXT PRIMARY KEY,
                    name TEXT
                )''')

                # Add the 'usn' column as the primary key if it doesn't exist
                cursor.execute('''PRAGMA table_info(students)''')
                columns = cursor.fetchall()
                existing_columns = [column[1] for column in columns]
                if 'usn' not in existing_columns:
                    cursor.execute('''ALTER TABLE students ADD COLUMN usn TEXT PRIMARY KEY''')

                # Add the 'name' column if it doesn't exist
                cursor.execute('''PRAGMA table_info(students)''')
                columns = cursor.fetchall()
                existing_columns = [column[1] for column in columns]
                if 'name' not in existing_columns:
                    cursor.execute('''ALTER TABLE students ADD COLUMN name TEXT''')

                # Get today's date
                today = datetime.date.today()
                column_name = f"col_{today.strftime('%Y_%m_%d')}"

                # Add the column with today's date if it doesn't exist
                cursor.execute('''PRAGMA table_info(students)''')
                columns = cursor.fetchall()
                existing_columns = [column[1] for column in columns]
                if column_name not in existing_columns:
                    cursor.execute(f"ALTER TABLE students ADD COLUMN {column_name} TEXT")

                # Check if x is present in the 'usn' column, and add it if not
                # Replace with the value you want to check
                cursor.execute("SELECT COUNT(*) FROM students WHERE usn = ?", (usn1,))
                result = cursor.fetchone()[0]
                if result == 0:
                    cursor.execute("INSERT INTO students (usn,name) VALUES (?, ?)", (usn1,name1))

                # Check if the cell associated with column_name in the row containing usn column value x is empty,
                # and add the current time if empty
                cursor.execute(f"SELECT {column_name} FROM students WHERE usn = ?", (usn1,))
                cell_value = cursor.fetchone()[0]
                if cell_value is None:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    cursor.execute(f"UPDATE students SET {column_name} = ? WHERE usn = ?", (current_time, usn1))

                conn.commit()
                ###mod1 end

            else:
                print("USN not found.")

            # Close the database connection
            conn.close()

            os.remove(image_path)
        except:
            os.remove(image_path)
            pass
        ####modification ends

    # Reset the running state of thread_1
    thread_1_running[0] = False

def detect_faces():
    
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    def process_frame():
        print("inside loop")
        
        ret, frame = cam.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if (time.time() - starting_time) > 1 and not thread_1_running[0]:
                for (x, y, w, h) in faces:
                    # Expand the region of interest (ROI) to include the forehead, hair, and ears
                    roi_x = max(0, x - int(w * 0.2))
                    roi_y = max(0, y - int(h * 0.3))
                    roi_w = min(frame.shape[1] - roi_x, int(w * 1.4))
                    roi_h = min(frame.shape[0] - roi_y, int(h * 1.6))

                    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)

                    # Capture the face image within the expanded ROI
                    face_image = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
                    face_image_path = f"tmp_folder/face_{time.time()}.png"
                    cv2.imwrite(face_image_path, face_image)

                # Start a new thread to process the captured images
                thread_1 = threading.Thread(target=process_images)
                thread_1.start()
                thread_1_running[0] = True

            # Convert the frame to RGB for Tkinter display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the image in the Tkinter label
            label.config(image=img_tk)
            label.image = img_tk

        if tk.Toplevel.winfo_exists(root):
            root.after(10, process_frame)
        else:
            # Stop the camera capture
            cam.release()
            cv2.destroyAllWindows()

    root = tk.Tk()
    root.title("Face Detection App")

    # Create a label to display the video frame
    label = tk.Label(root)
    label.pack()

    root.protocol("WM_DELETE_WINDOW", root.quit)

    process_frame()

    # Start the Tkinter event loop
    root.mainloop()

detect_faces()
