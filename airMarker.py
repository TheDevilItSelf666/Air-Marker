
import random
import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

folder_path = "Header"
myList = os.listdir(folder_path)
#print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folder_path}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))
colorList = [(255, 0, 255), (0, 255, 0), (0, 255, 255), (0, 0, 255)]
header = overlayList[0]
header = cv2.resize(header, (1280, 125))
drawColor = (255, 0, 255)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detection_con=0.85)
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        #print(lmList)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersup()
        print(fingers)

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            print("seletion mode")
            if y1 < 125:
                if 150 < x1 < 350:
                    header = overlayList[0]
                    header = cv2.resize(header, (1280, 125))
                    drawColor = (255, 0, 255)
                elif 470 < x1 < 550:
                    header = overlayList[1]
                    header = cv2.resize(header, (1280, 125))
                    drawColor = (0, 255, 0)
                elif 700 < x1 < 750:
                    header = overlayList[2]
                    header = cv2.resize(header, (1280, 125))
                    drawColor = (0, 255, 255)
                elif 900 < x1 < 1000:
                    header = overlayList[3]
                    header = cv2.resize(header, (1280, 125))
                    drawColor = (0, 0, 255)
                elif 1150 < x1 < 1200:
                    header = overlayList[4]
                    header = cv2.resize(header, (1280, 125))
                    drawColor = (0, 0, 0)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
            print("Drawing mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0,):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, 80)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 80)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, 15)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, 15)
            xp, yp = x1, y1
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            imgCanvas[:, :] = (0, 0, 0)
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("image", img)
    #cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)
