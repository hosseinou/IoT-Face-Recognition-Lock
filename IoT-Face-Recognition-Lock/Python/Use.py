import cv2

import pickle
import socket
import threading

connectioList = []


def showFace():
    while True:
        cv2.waitKey(48)
        ret, frame2 = camera.read()
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x1, y1, w1, h1) in faces:
            roi_gray1 = gray[y1:y1 + h1, x1:x1 + w1]
            sname1 = ""
            id_1, conf1 = recognizer.predict(roi_gray1)
            for name1, value1 in dict.items(dicti):
                if value1 == id_1:
                    sname1 = name1
                    break

            if conf1 <= 48:
                print("OPEN : " + sname1 + " : " + str(conf1))
                frame2 = cv2.rectangle(frame2, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                frame2 = cv2.putText(frame2, sname1 + str(conf1), (x1, y1), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                frame2 = cv2.putText(frame2, "Press any key to Open the door", (10, 10), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                print("Face Detected")
                cv2.imshow('frame', frame2)
                cv2.waitKey(0)
                for c in connectioList:
                    c.send("OPENM".encode())
                return
            else:
                frame2 = cv2.rectangle(frame2, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                cv2.imshow('frame', frame2)
                print("Close ")


def socketServerRun(s1):
    """
    function to print cube of given num
    """
    while True:
        # Establish connection with client.

        c, addr = s1.accept()
        connectioList.append(c)
        print('Got connection from', addr)


with open('labels', 'rb') as f:
    dicti = pickle.load(f)
    f.close()

camera = cv2.VideoCapture(0)
s = socket.socket()
s.bind(('', 1250))
s.listen(5)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

font = cv2.FONT_HERSHEY_SIMPLEX
t1 = threading.Thread(target=socketServerRun, args=(s,))
t1.start()
while True:
    print("Start Detection : Press Any key to start Detection")
    frame = cv2.imread("9.jpg", cv2.IMREAD_COLOR)
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    while True:
        ret1, frame1 = camera.read()
        frame1 = cv2.putText(frame1, "Set your face Press Enter When You was ready", (10, 10), font, 0.5, (0, 0, 255),
                             2, cv2.LINE_AA)
        cv2.imshow("frame", frame1)
        key1 = cv2.waitKey(30)
        if key1 == 13:
            break
    showFace()