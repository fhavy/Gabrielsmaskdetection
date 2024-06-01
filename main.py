import cv2
import cvzone
import os
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480) 

detector = HandDetector(staticMode=False , maxHands=1,detectionCon=0.7)

#Importing all mode images
imgBackground = cv2.imread('background.png')
folderPathModes = "Modes"
listImgModesPath = os.listdir('Modes')

listImgModes = []

for imgModesPath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModesPath)))

#Importing all Icon images
folderPathIcons = "Icons"
listImgIconsPath = os.listdir('Icons')
listImgIcons = []

for ImgIconsPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons,ImgIconsPath)))
# For changing selection mode
modeType = 0
selection = -1
counter = 0
selectionSpeed = 7
modePositions = [(1020+450,540),(1247,354),(1247,623),(1247,903),(1689,354),(1689,623),(1689,903)]
ellipsePositions = [(180,180),(84,84)]
counterPause = 0
selectionList = [-1,-1,-1,-1]

while True:
    success,img = cap.read()
    
    #Hand tracker
    hands, img = detector.findHands(img)

    #Overlay webcam over background image
    imgBackground[360:360+480,144:144+640] = img
                 # height      width
    imgBackground[0:1080,1020:1920] = listImgModes[modeType]

    if hands and counterPause == 0 and modeType<4 and modeType!=0:
        hand = hands[0]
        bbox = hand['bbox']
        lmList = hand['lmList']
        center = hand['center']
        handType = hand['type']

        fingers = detector.fingersUp(hand)

        
        if fingers == [0,1,0,0,0]:
            if selection !=1:
                counter = 1
            selection = 1
        elif fingers == [0,1,1,0,0]:
            if selection !=2:
                counter = 1
            selection = 2
        elif fingers == [0,1,1,1,0]:
            if selection !=3:
                counter = 1
            selection = 3
        elif fingers == [0,1,1,1,1]:
            if selection !=4:
                counter = 1
            selection = 4
        elif fingers == [1,1,1,1,1]:
            if selection !=5:
                counter = 1
            selection = 5
        elif fingers == [1,0,0,0,0]:
            if selection !=6:
                counter = 1
            selection = 6
        else:
            selection = -1
            counter = 0

        if counter>0:
            counter+=1
        
            cv2.ellipse(imgBackground,modePositions[selection],ellipsePositions[1],0,0,counter*selectionSpeed,(20,29,43),13)
        

            if counter*selectionSpeed>360:
                selectionList[modeType-1] = selection
                modeType+=1
                counter = 0 
                selection = -1
                counterPause = 1

    elif hands and counterPause == 0 and modeType == 0:
        hand = hands[0]
        bbox = hand['bbox']
        lmList = hand['lmList']
        center = hand['center']
        handType = hand['type']

        fingers = detector.fingersUp(hand)

        if fingers == [1,0,0,0,1]:
            if selection !=0:
                counter = 1
            selection = 0
            
        else:
            selection = -1
            counter = 0
            
        if counter>0:
            counter+=1
        
            cv2.ellipse(imgBackground,modePositions[selection],ellipsePositions[0],0,0,counter*selectionSpeed,(20,29,43),13)
        

            if counter*selectionSpeed>360:
                modeType+=1
                counter = 0 
                selection = -1
                counterPause = 1

    # To pause after each selection
    if counterPause>0:
        counterPause+=1
        if counterPause>60:
            counterPause = 0
            
    
    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[957:957+98,135:135+98] = listImgIcons[selectionList[0] - 1]
    
    if selectionList[1] != -1:
        imgBackground[957:957+98,321:321+98] = listImgIcons[5 + selectionList[1]]
    
    if selectionList[2] != -1:
        imgBackground[957:957+98,508:508+98] = listImgIcons[11 + selectionList[2]]
     
    checkImg = cv2.imread('check.png')

    if modeType == 4 and selectionList[3] == -1:
        imgBackground[957:957+98,694:694+98] = checkImg

    #Displaying image
    cv2.imshow("Background",imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break