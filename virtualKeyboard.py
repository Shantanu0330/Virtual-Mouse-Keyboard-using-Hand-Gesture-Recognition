import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep 
import numpy as np
import cvzone
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

def rescale_frame(frame, percent=2):
    width = int(frame.shape[1] * percent)
    height = int(frame.shape[0] * percent)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

detector = HandDetector(detectionCon = 0.8)    

keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["!", "@", "#", "$", "%", "^", "&", "=", "{", "}"]]

finalText = ""
 
keyboard = Controller()
 
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img
 
class Buttons():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text
 
 
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Buttons([100 * j + 50, 100 * i + 50], key))
 
while True:
    rect, frame = cap.read()
    img = rescale_frame(frame, percent=2)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)
 
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
 
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                #print(l)
 
                ## when clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, tuple(button.pos), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.07)
 
    #cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    #cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
