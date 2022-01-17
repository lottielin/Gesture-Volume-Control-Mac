import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, minDetectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC,
                                        self.minDetectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:  
                if draw:  
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        lmList = []
        if self.results.multi_hand_landmarks:
            currHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(currHand.landmark):
                xPos = int(lm.x * imgWidth)
                yPos = int(lm.y * imgHeight)
                lmList.append([id, xPos, yPos])
                """ if draw:
                    cv2.putText(img, str(id), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1) """

        return lmList

def main():
    
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        ret, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList:
            print(lmList[4])
    
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 1)

        if ret:
            cv2.imshow('Camera', img)

        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    main()