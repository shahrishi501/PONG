import numpy as np 
import cv2 as cv
import cvzone
from cvzone.HandTrackingModule import HandDetector

capture = cv.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

capture.set(3, 1280)
capture.set(4, 720)

background = cv.imread('Resources/Background.png')
ball = cv.imread('Resources/Ball.png', cv.IMREAD_UNCHANGED)
bat1 = cv.imread('Resources/Bat1.png', cv.IMREAD_UNCHANGED)
bat2 = cv.imread('Resources/Bat2.png', cv.IMREAD_UNCHANGED)
gameOver = cv.imread('Resources/GameOver.png')

position = [100, 100]
isOver = False
speedX, speedY = 30,30
score = [0, 0]

while True: 
    # read() function returns the frame and the boolean value that says whether the frame was read successfully or not.
    # We flip the image horizontally to avoid confusion due to lateral inversion.
    isTrue, frame = capture.read()
    frame = cv.flip(frame, 1)

    # To detect hands and its landmarks, without any annotations. findHands returns a boolean value.
    hands, frame = detector.findHands(frame, flipType = False)

    # For overlaying images.
    # addWeighted() puts the foreground image with an amount of transparency on top of the underlying image.
    # In this case, our underlying image at every instant is the camera feed.
    frame = cv.addWeighted(frame, 0.5, background, 0.5, 0.0) 

    # Check for hands. Hands is a dictionary, so we process it like one.
    if hands:
        for hand in hands:
            # Gets the positional values of hand in bounding box.
            x, y, w, h = hand['bbox'] 
            h1, w1, _ = bat1.shape  # To get height and width of the bat
            y1 = y - h1//2  # To ensure your hands are at center of the bat.
            # Clips the value to ensure overlays don't occur outside the pop-up space.
            y1 = np.clip(y1, 20, 415)
            # Draw the bats
            if hand['type'] == 'Left':
                frame = cvzone.overlayPNG(frame, bat1, (59, y1))
                if (59 < position[0] < 59 + w1) and (y1 < position[1] < y1 + h1):
                    # If bat hits the ball, reverse the ball direction along x-axis.
                    speedX = -speedX
                    position[0] += 20
                    score[0] += 1

            if hand['type'] == 'Right':
                frame = cvzone.overlayPNG(frame, bat2, (1195, y1))
                if (1145 < position[0] < 1165) and (y1 < position[1] < y1 + h1):
                    speedX = -speedX
                    position[0] -= 20
                    score[1] += 1

    # If ball goes out of bounds, game's over.
    if position[0] < 40 or position[0] > 1195:
        isOver = True

    if isOver:
        frame = gameOver
        cv.putText(frame, str(score[1] + score[0]).zfill(2), (585, 360), cv.FONT_HERSHEY_COMPLEX,
                   2.5, (200, 0, 200), 5)  # (200, 0, 200) gives purple colour
    else:
        # Move the ball. If the ball hits the wall of upper rectangle, reverse its direction along y-axis.
        if position[1] >= 500 or position[1] <= 10:
            speedY = -speedY

        # We give the ball speed.
        position[0] += speedX
        position[1] += speedY

        # Draw the ball
        frame = cvzone.overlayPNG(frame, ball, position)

        # Display score as game goes on. we use putText() for this. (255, 255, 255) is white colour
        cv.putText(frame, str(score[0]), (300, 650),
                   cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv.putText(frame, str(score[1]), (900, 650),
                   cv.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    # imshow() function returns the matrix of pixels in a new window. It also takes the name of the popup window.
    cv.imshow('Pong game', frame)
    # waitKey() function allows the popup window to be displayed for a certain time period in milliseconds.
    key = cv.waitKey(1)
    # If R is pressed, re-initialise the respective variables and restart the game.
    if key == ord('r'):
        position = [100, 100]
        speedX = 10
        speedY = 10
        isOver = False
        score = [0, 0]
        gameOver = cv.imread('Resources/GameOver.png')

    # To quit the game
    if key == ord('q'):
        break

# Release the capture and close all OpenCV windows
capture.release()
cv.destroyAllWindows()


      