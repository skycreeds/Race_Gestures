import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 210)

detector = HandDetector(detectionCon=0.75, maxHands=2)
keyboard = Controller()


while True:
    _, img = cap.read()
    hands, img = detector.findHands(img, flipType=True)
    # When hands are there in frame
    if hands:
        # Segregating hands
        if(hands[0]['type']=="Right"):
            right = detector.fingersUp(hands[0])
        if(hands[0]['type']=="Left"):
            left = detector.fingersUp(hands[0])
        if len(hands)==2:
            if (hands[1]['type'] == "Right"):
                right2 = detector.fingersUp(hands[1])
            if (hands[1]['type'] == "Left"):
                left2 = detector.fingersUp(hands[1])

        # Right hand Decelerate + Accelerate
        if right == [0,0,0,0,0] or right2 == [0,0,0,0,0]:
            keyboard.press(Key.down)
            keyboard.release(Key.up)
        elif right == [1,1,1,1,1] or right2 == [1,1,1,1,1]:
            keyboard.press(Key.up)
            keyboard.release(Key.down)
        else:
            keyboard.release(Key.up)
            keyboard.release(Key.down)

        # Left hand Center + Left + Right
        if left == [1,0,0,0,0] or left2 == [1,0,0,0,0]:
            keyboard.press(Key.right)
            keyboard.release(Key.left)
        elif left == [1,1,1,1,1] or left2 == [1,1,1,1,1]:
            keyboard.press(Key.left)
            keyboard.release(Key.right)
        elif left == [0, 0, 0, 0, 0] or left2 == [0,0,0,0,0]:
            keyboard.release(Key.left)
            keyboard.release(Key.right)
        else:
            keyboard.release(Key.left)
            keyboard.release(Key.right)

    # When there are no hands in frame
    else:
        keyboard.release(Key.up)
        keyboard.release(Key.down)
        keyboard.release(Key.right)
        keyboard.release(Key.left)

    cv2.imshow("Gesture Based Game", img)
    right = None
    left = None
    right2 = None
    left2 = None
    if cv2.waitKey(1) == ord("q"):
        break