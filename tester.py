import cv2
import sqlite3

font = cv2.FONT_HERSHEY_SIMPLEX
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def getProfile(id):
    conn = sqlite3.connect("Face database.db")
    cmd = "SELECT * FROM USER WHERE ID=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    rec = cv2.face.LBPHFaceRecognizer_create()
    # read yml file to test the input and predict
    rec.read("trainedData.yml")
    path = 'Face-dataset'
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            id, confidence = rec.predict(gray[y:y + h, x:x + w])
            profile = getProfile(id)
            if profile != None:
                cv2.putText(img, str(profile[0]), (x - 30, y + h + 30), font, 1, (255, 255, 255))
                cv2.putText(img, str(profile[1]), (x, y + h + 30), font, 1, (255, 255, 255))
                cv2.putText(img, "AGE " + str(profile[2]), (x + h, y + h + 30), font, 1, (255, 255, 255))
                cv2.putText(img, str(profile[3]), (x, y + h + 60), font, 1, (255, 255, 255))
                cv2.putText(img, "Confidence: " + str(confidence), (x, y - h + 60), font, 1, (255, 255, 255))
        # subitems = smile_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in subitems:
        #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imshow("Face", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
