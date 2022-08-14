
from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np
import autopy
import time

wCam, hCam = 640, 480
frameR = 100
smoothening = 5

plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)

isLeftClick = False

cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = HandDetector(detectionCon=0.75, maxHands=1)

while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    fpsString = f"FPS: {int(fps)}"
    cv2.putText(img, fpsString, (20,50), cv2.FONT_HERSHEY_PLAIN, 2.3, (255,0,0), 3)


    hands, img, lmList = detector.findHands(img)

    if hands:
        indexFingerX, indexFingerY = lmList[8][0], lmList[8][1]
        middleFingerX, middleFingerY = lmList[12][0], lmList[12][1]


        print(f"{indexFingerX} {indexFingerY}")
        # print(lmList[8])

        fingers = detector.fingersUp(hands[0])
        print(fingers)

        cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (0,255,0), 2 )


        if fingers[1] == 1 and fingers[2] == 0:

            mouseX = np.interp(indexFingerX, [frameR, wCam-frameR], [0, autopy.screen.size()[0]])
            mouseY = np.interp(indexFingerY, [frameR, hCam-frameR], [0, autopy.screen.size()[1]])

            clocX = plocX + (mouseX - plocX) / smoothening
            clocY = plocY + (mouseY - plocY) / smoothening

            autopy.mouse.move(autopy.screen.size()[0] - clocX, clocY)

            cv2.circle(img, (indexFingerX, indexFingerY), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            isLeftClick = False
        if fingers[1] == 1 and fingers[2] == 1:
            length, info, img = detector.findDistance((lmList[8][0],lmList[8][1]), (lmList[12][0], lmList[12][1]), img)

            if length < 40 and not isLeftClick:
                cv2.circle(img, (info[4], info[5]), 15, (0, 255, 255), cv2.FILLED)
                autopy.mouse.click()
            isLeftClick = True
            print(length)

        autopy.mouse.toggle(button=autopy.mouse.Button.RIGHT, down=False)

        

    if hands:
        # print(detector.fingersUp(hands[0]))
        fingers_up_list = detector.fingersUp(hands[0])
        # print(lmList)
    # else:
    #     arduino.sendData([0, 0, 0, 0, 0])

    cv2.imshow('Image', img)
    cv2.waitKey(1)