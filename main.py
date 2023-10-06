import cv2
import cvzone
import mediapipe
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot





cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1) #face counter
plotY = LivePlot(640,360,[0,0.45])
plotratio = LivePlot(640,480,[10,100.0])
#idlist = [130,247,30,29,27,28,55,24,23,22,26,112]
#idlist = [33,246,161,160,159,158,157,173,133,7,163,144,145,153,154,155,362,398,384,385,386,387,388,466,263,249,390,373,374,380,381,382,362] #eyeball
idlist = [33,246,161,159,158,157,173,155,154,153,145,144,163,7]



def compute(x,y):
    x = np.array(x)
    y = np.array(y)
    dist = np.linalg.norm(x - y)
    return dist

def blinked(a,b,c,d):
    short = compute(a,b)
    long = compute(c,d)
    ratio = short/(2.0*long)
    return ratio

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,2)
    success, img = cap.read()

    img, faces = detector.findFaceMesh(img,draw=False)

    if faces:
        face = faces[0]
        for id in idlist:
            cv2.circle(img,face[id],1,(255,0,255),2,cv2.FILLED)

        leftup = face[159]
        leftdown = face[145]
        leftleft = face[33]
        leftright = face[133]
        ratioe =blinked(face[27],face[145],face[33],face[133])
        print(ratioe)
        #lenho ,_ = detector.findDistance(leftleft,leftright)
        #lenver ,_ = detector.findDistance(leftup,leftdown)
        #print("VErt ",lengver)
        #print("Hori ",lenfthhor)

        #cv2.line(img,leftup,leftdown,(0,255,0),2)
        #cv2.line(img,leftleft,leftright,(0,255,0),2)
        cv2.rectangle(img,(leftup),(leftdown),(0,255,0),2)
        #cv2.line(img,leftleft,leftright,(0,455,0),2)
        #ratio = (lenver/lenho)*100
       # print("Ratio:- ",ratio)
        #disl = lenleho
       # disr = lenho
        #print("LEft eye ",disl)
        #print("Right eye ",disr)
        #print(blinked)
        imgploatl = plotY.update(ratioe)
        cv2.imshow("imgploat1",imgploatl)
        #ratioploat = plotratio.update(ratio)
        #cv2.imshow("ratioploat",ratioploat)
        #imgploatr = plotY.update(disr)
       # cv2.imshow("imgploat",imgploatl)
        #cv2.imshow("imgploatr",imgploatr)
    #cv2.resize(img,(640,360))

    cv2.imshow('image',img)
    cv2.waitKey(2)
