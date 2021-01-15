import cv2
import numpy as np
import os
import sqlite3


def InsertIntoDB(nam, age, dob):
    search_query = "SELECT * FROM USER WHERE NAME ='" + nam + "'"
    cursor = conn.execute(search_query)
    for row in cursor:
        # row exists
        print("Similar name found")
        return False
    query = "INSERT INTO USER (`NAME`,`AGE`,`DOB`) VALUES ('" + nam + "'," + age + ",'" + dob + "')"
    conn.execute(query)
    conn.commit()
    return True


if __name__ == '__main__':
    # connect database
    conn = sqlite3.connect("Face database.db")
    # Enter details
    Uname = input("Enter your name")
    Uage = input("Enter your age")
    Udob = input("Enter your DOB YYYY-MM-DD format")
    # update database
    if InsertIntoDB(Uname, Uage, Udob):
        # create a directory for the entered name, so that we can collect the Images.
        cursor = conn.execute("SELECT * FROM USER WHERE NAME ='" + Uname + "'")
        #Get the ID of added user for saving the images
        for row in cursor: ID = row
        ID = int(ID[0])
        # print(ID)
        BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
        # print(BASE_DIRECTORY)
        BASE_DIRECTORY = BASE_DIRECTORY + "\Face-dataset"
        IMAGE_DIRECTORY = os.path.join(BASE_DIRECTORY, str(Uname))
        #Make a different folder of the added user
        os.mkdir(IMAGE_DIRECTORY)
        # print(IMAGE_DIRECTORY,type(IMAGE_DIRECTORY))
        #use haar cascade to detect the face in the video input
        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)
        image_count = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray)
            faces = faceDetect.detectMultiScale(gray, 1.0485258, 6)
            #detect face and store 50 images into Face-dataset folder
            #the path for the image will be Face-dataset/username/ID.1
            #the path for the image will be Face-dataset/username/ID.2 and so on
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imwrite(IMAGE_DIRECTORY + "/" + str(ID)+ "."+str(image_count) + ".jpg", gray[y:y + h, x:x + w])
                cv2.waitKey(100)
            cv2.imshow("Face", img)
            image_count += 1
            if image_count == 50:
                break
        conn.close()
        cam.release()
        cv2.destroyAllWindows()
    else:
        print("Failed to add your data Try again...")
