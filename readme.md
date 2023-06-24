==========================================================================================================================
# Libraries required													 
--------------------------------------------------------------------------------------------------------------------------
1. Deepface														 
    pip install deepface											         
2. opencv                                                                                                                
    pip install opencv-python                                                                                            
3. tkinter                                     							                         
    pip install tk
4. Sqlite    
    pip install db-sqlite3
5. openpyxl
    pip install openpyxl
6. PIL
    pip install  pillow    
    
=========================================================================================================================
# steps to run
1 first run the capture.py file take usn,name  to enroll images
2 then run recog.py which will recognise the faces and update database
3 run toexcel.py to generate excel sheets of attendace


==========================================================================================================================
# SUMMARY

This program aims in creating an attendance system using Face recognition with the use of deepface framework.
deepface directly provides us with below mentioned face recognition models

  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",

In this program we make use of "Facenet" model developed by google for face recognition as we found it best among these.
We use deepface find method to check if the face in given image is present among the images in  database(folder)


=========================================================================================================================
# capture.py
In this code we area creating a tkinter app and the following things happen inside the app
    1. creating a database "attendance.db"  if not exists
    2. creating a table "image_labels" inside the database containing the columns "image_name","usn","name"
    3. collect usn and name from the user capture image and store it in a folder "my_db"
        the name for  image is randomly generated and the path to image is stored in a cell in "img_name" column of
        "image_labels"
        table and usn and name in corresponding cells of the same row
    4. while capturing  remove if some pre existing image representations are present, that is some file ending with ".pkl"
# -------------------------------------------------------------------------------------------------------------------------

# recog.py
using oencv embedded in tkinter app capture video, with interval of few seconds/milliseconds capture frames and capture each 
faces and store in a folder , another thread will use deepface find funtion for each face images in the folder and if it 
matches the path to the matching image in image database(folder) is retrieved from the returned value and identifies usn 
from image_labels table and will add it to the students table
# --------------------------------------------------------------------------------------------------------------------------

# toexcel.py
To convert the students table to an excel sheet

=============================================================================================================================
