#Main Graphical User Interface for the Multi Spectral Tomography system

import PySimpleGUI as sg
import sys
import serial
from serial.tools.list_ports import comports
import cv2
import threading
import time

#Setting up the arduino to the first com port.
serialList = [p.device for p in comports()]
ser = serial.Serial(serialList[0])

#setting the video capture devices. note that usually the '0' camera
#is a built in webcam and thus the plugged in cams enumerate from 1 to 2
video_capture_1 = cv2.VideoCapture(1)
video_capture_2 = cv2.VideoCapture(2)

#set camera parameters
video_capture_1.set(3,1920)
video_capture_1.set(4,1080)

video_capture_2.set(3,2592)
video_capture_2.set(4,1944)

time.sleep(2) #give the cameras time to make the resolution setting

while True:
    # Capture frame-by-frame
    ret1, frame1 = video_capture_1.read() #grayscale video streamed
    ret2, frame2 = video_capture_2.grab() #colour video only captured on trigger

    if (ret1):
        # Display the resulting frame
        grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Cam 1', grayscale1)

#    if (ret2):
#        # Display the resulting frame
#        cv2.imshow('Cam 2', frame2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows()