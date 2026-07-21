import cv2
import numpy as np
import os
import sys

vid = cv2.VideoCapture(0)
# rawCapture = PiRGBArray(camera, size=(640, 480))

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

name = input("What's his/her Name? ")
dirName = "./images/" + name
print(dirName)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory Created")
else:
    print("Name already exists")
    sys.exit()

count = 1
ret, frame = vid.read()
cv2.imshow("face", frame)
key = cv2.waitKey(0)
while True:
    ret, frame = vid.read()
    if count > 30:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        roiGray = gray[y:y + h, x:x + w]
        fileName = dirName + "/" + name + str(count) + ".jpg"
        cv2.imwrite(fileName, roiGray)
        cv2.imshow("face", roiGray)
        key = cv2.waitKey(5)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count += 1
        print(count)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(30)

    if key == 27:
        break

cv2.destroyAllWindows()
sys.exit()