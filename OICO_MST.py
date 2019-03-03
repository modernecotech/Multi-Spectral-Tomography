#Main Graphical User Interface for the Multi Spectral Tomography system

import PySimpleGUIQt as sg
import sys
import serial
from serial.tools.list_ports import comports
import cv2
import threading
import time
from configparser import SafeConfigParser

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

time.sleep(1) #give the cameras time to make the resolution setting
ser.write(str.encode('0')) #start the IR 770nm on arduino

#read in the saved configuration details for default folder, operator, etc
config=SafeConfigParser()
config.read('config.ini')
defaultOperatorName = config[DEFAULT][OperatorName]
defaultOperatorID = config[DEFAULT][OperatorID]
defaultFolder = config[DEFAULT][DefaultFolder]

#starting up the GUI
menu_def=[
    ['File', ['Operation Setup','System Setup']],
    ['Help','About']
]

illumination_frame=[
    [sg.Text('',size=(8,0)),sg.Radio('',"RADIO2",key='a')],
    [sg.Text('',size=(3,0)),sg.Radio('',"RADIO2",key='l'),sg.Text('',size=(4,0)),sg.Radio('',"RADIO2",key='b')],
    [sg.Text('',size=(1,0)),sg.Radio('',"RADIO2",key='k'),sg.Text('',size=(8,0)),sg.Radio('',"RADIO2",key='c')],
    [sg.Radio('',"RADIO2",key='j'),sg.Text('',size=(3,0)),sg.Radio('OFF',"RADIO2",key='m',default=True),sg.Text('',size=(1,0)),sg.Radio('',"RADIO2",key='d')],
    [sg.Text('',size=(1,0)),sg.Radio('',"RADIO2",key='i'),sg.Text('',size=(8,0)),sg.Radio('',"RADIO2",key='e')],
    [sg.Text('',size=(3,0)),sg.Radio('',"RADIO2",key='h'),sg.Text('',size=(4,0)),sg.Radio('',"RADIO2",key='f')],
    [sg.Text('',size=(8,0)),sg.Radio('',"RADIO2",key='g')],
]

layout = [
    [sg.Menu(menu_def,tearoff=True)],
    [sg.Text('Ophthalmic Instrument Company MST', size=(40,1), justification='center',font=('Helvetica','16'))],
    [sg.Text('Folder to store images',size=(15,1)), sg.Input(key='_storageFolder_',default_text=defaultFolder), sg.FolderBrowse()],
    [sg.Text('Operator Name',size=(15,1)),sg.InputText(key='operatorName',default_text=defaultOperatorName)],
    [sg.Text('Operator ID',size=(15,1)),sg.InputText(key='operatorID',default_text=defaultOperatorID)],
    [sg.VerticalSeparator()],
    [sg.Text('Patient Name',size=(15,1)),sg.InputText(key='PatientName')],
    [sg.Text('Patient Number',size=(15,1)),sg.InputText(key='PatientID')],
    [sg.Text('Patient Date of Birth',size=(15,1)),sg.Input(key='_dob_'),sg.CalendarButton('date of birth','_dob_')],
    [sg.Text('Eye Selection',size=(15,1)),sg.Radio('Left Eye',"RADIO1",default=True,key='_LeftEye_'),sg.Radio('Right Eye',"RADIO1",key='_RightEye_')],
    [sg.VerticalSeparator()],
 #   [sg.Frame('External Fixation', illumination_frame, font="Any 14", title_color='blue')],
    [sg.Text("External Fixation LEDs")],
    [sg.Dial((1,13),key="ext",enable_events=True,size=(150,150))],
    [sg.Text("OFF")],
    [sg.Button(button_text='Capture Image')],
    [sg.VerticalSeparator()],
    [sg.Quit()]
]

window = sg.Window('OICO MST').Layout(layout)
window.Location=(0,0)



def ImageCapture():
    ser.write(str.encode('2')) #start flash sequence
    t=time.strftime("%H%M%S")
    eyeselection = "L" if values['_LeftEye_'] is True else "R"
    filenameStart=(values['_storageFolder_'] + '/' + values['PatientName'] + values['PatientID'] + eyeselection + "_" + t)
    ret1, frame1 = video_capture_1.read()
    grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filenameStart + '770.png',grayscale1)
    ret1, frame1 = video_capture_1.read()
    grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filenameStart + '850nm.png',grayscale1)
    ret1, frame1 = video_capture_1.read()
    grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filenameStart + '810nm.png',grayscale1)
    ret2, frame2 = video_capture_2.read()
    cv2.imwrite(filenameStart + '520nm.png',frame2)    



while True:
    # Capture frame-by-frame
    ret1, frame1 = video_capture_1.read() #grayscale video streamed
    ret2, frame2 = video_capture_2.read() #colour video only captured 
    event, values = window._ReadNonBlocking() #
    
    if (ret1):
        # Display the resulting frame
        grayscale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow("Cam 1", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Cam 1", 1000,600)
        cv2.imshow('Cam 1', grayscale1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if event == 'Quit':
        break

    if event == 'Operation Setup':
        sg.PopupQuickMessage("some text operation setup key")

    if event == 'About':
        sg.PopupQuickMessage("The OICO MST was developed and made by Ophthalmic Instrument Company www.oico.co.uk")

    if event == 'Capture Image':
        ImageCapture()
    
    if values['ext'] == '1':
        ser.write(str.encode("m"))

    if values['ext'] == '2':
        ser.write(str.encode("a"))

    if values['ext'] == '3':
        ser.write(str.encode("b"))

    if values['ext'] == '4':
        ser.write(str.encode("c"))

    if values['ext'] == '5':
        ser.write(str.encode("d"))

    if values['ext'] == '6':
        ser.write(str.encode("e"))

    if values['ext'] == '7':
        ser.write(str.encode("f"))

    if values['ext'] == '8':
        ser.write(str.encode("g"))

    if values['ext'] == '9':
        ser.write(str.encode("h"))

    if values['ext'] == '10':
        ser.write(str.encode("i"))

    if values['ext'] == '11':
        ser.write(str.encode("j"))

    if values['ext'] == '12':
        ser.write(str.encode("k"))
        
    if values['ext'] == '13':
        ser.write(str.encode("l"))


# When everything is done, release the capture
video_capture_1.release()
video_capture_2.release()
cv2.destroyAllWindows()
ser.write(str.encode('1')) #switch off all LEDs
ser.close()
window.Close()
