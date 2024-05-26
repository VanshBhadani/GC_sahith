import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

width, height = 1280, 720
folderPath = "presentation"

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

pathImages = sorted(os.listdir(folderPath), key=len)
# print(pathImages)

imgNumber = 0
hs, ws = int(120*1), int(213*1)
gt = 300
buttonPress = False
counter = 0
Delay = 15
annos = [[]] # annos is annotations its meaning is a note by way of explanation or comment added to a text or diagram.
annoNum = -1
annoStart = False

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gt), (width, gt), (134, 255, 67), 7)

    if hands and buttonPress is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cenx, ceny = hand['center']
        lmList = hand['lmList']

        xVal = int(np.interp(lmList[8][0], [width // 2, w-100], [0, width]))
        yVal = int(np.interp(lmList[8][1], [220, height-220], [0, height]))
        indexFinger = xVal, yVal
        if ceny <= gt:

            if fingers == [1, 0, 0, 0, 0]:
                annoStart = False
                print('left')

                if imgNumber > 0:
                    buttonPress = True
                    annos = [[]]
                    annoNum = -1
                    imgNumber -= 1

            if fingers == [0, 0, 0, 0, 1]:
                annoStart = False
                print('right')

                if imgNumber < len(pathImages)-1:
                    buttonPress = True
                    annos = [[]]
                    annoNum = -1
                    imgNumber += 1

        # pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annoStart = False


        #Drawer
        if fingers == [0, 1, 0, 0, 0]:
            if annoStart is False:
                annoStart = True
                annoNum += 1
                annos.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annos[annoNum].append(indexFinger)

        else:
            annoStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annos:
                annos.pop(-1)
                annoNum -= 1
                buttonPress = True

    else:
        annoStart = False

    if buttonPress:
        counter += 1
        if counter > Delay:
            counter = 0
            buttonPress = False

    for i in range(len(annos)):
        for j in range(len(annos[i])):
            if j != 0:
                cv2.line(imgCurrent, annos[i][j - 1], annos[i][j], (255, 255, 255), 8)


    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall

    cv2.imshow("Presentation", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break



