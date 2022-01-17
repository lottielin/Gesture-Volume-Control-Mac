import cv2
import time
import numpy as np
import math
import handTrack as ht
import osascript as osa

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cTime = 0
pTime = 0
vol = 0
barVol = 400

detector = ht.handDetector(minDetectionCon=0.7)

while cap.isOpened():
    ret, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    # Thumb tip: 4
    # Index finger tip: 8
    if lmList:
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        indexX, indexY = lmList[8][1], lmList[8][2]
        midX, midY = (thumbX+indexX)//2, (thumbY+indexY)//2

        cv2.circle(img, (thumbX, thumbY), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (indexX, indexY), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (midX, midY), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (thumbX, thumbY), (indexX, indexY), (255, 0, 255), 2)

        finDiff = math.hypot(indexX-thumbX, indexY-thumbY)
        # print(finDiff)
        # manual range: 20 - 200
        finDiffMin = 20
        finDiffMax = 200
        if finDiff < 30:
            cv2.circle(img, (midX, midY), 10, (255, 0, 0), cv2.FILLED)

        # osascript package usage: osascript.run('set volume output volume 50')
        minVol = 0
        maxVol = 100
        vol = np.interp(finDiff, [finDiffMin, finDiffMax], [minVol, maxVol])
        osa.run(f'set volume output volume {str(int(vol))}')

        barVol = np.interp(finDiff, [finDiffMin, finDiffMax], [400, 150])

   
    cv2.rectangle(img, (50, 150), (85, 400), (255, 120, 0), 3)
    cv2.rectangle(img, (50, int(barVol)), (85, 400), (255, 120, 0), cv2.FILLED)
    cv2.putText(img,f'{str(int(vol))} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 120, 0), 2)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    if ret:
        cv2.imshow('Camera', img)
    if cv2.waitKey(1) == ord('q'):
        break