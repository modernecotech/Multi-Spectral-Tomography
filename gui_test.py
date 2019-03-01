import PySimpleGUI as sg 

menu_def=[
    ['File', ['Operation Setup','System Setup']],
    ['Help','About']
]

layout = [
    [sg.Menu(menu_def,tearoff=True)],
    [sg.Text('Ophthalmic Instrument Company MST', size=(40,1), justification='center',font=('Helvetica','20'))],
    [sg.Text('Folder to store images',size=(15,1)), sg.Input(key='_storageFolder_'), sg.FolderBrowse()],
    [sg.Text('Operator Name',size=(15,1)),sg.InputText(key='operatorName')],
    [sg.Text('Operator ID',size=(15,1)),sg.InputText(key='operatorID')],
    [sg.VerticalSeparator()],
    [sg.Text('Patient Name',size=(15,1)),sg.InputText(key='PatientName')],
    [sg.Text('Patient Number',size=(15,1)),sg.InputText(key='PatientID')],
    [sg.Text('Patient Date of Birth',size=(15,1)),sg.Input(key='_dob_'),sg.CalendarButton('date of birth','_dob_')],
    [sg.Text('Eye Selection',size=(15,1)),sg.Radio('Left Eye',"RADIO1",default=True,key='_LeftEye_'),sg.Radio('Right Eye',"RADIO1",key='_RightEye_')],
    [sg.VerticalSeparator()],
    [sg.Button(button_text='Capture Image')],

    [sg.Quit()]
]

window = sg.Window('OICO MST').Layout(layout)

while True:
    event, values = window.ReadNonBlocking()
    if event == 'Quit':
        break
    if event == 'Operation Setup':
        sg.PopupQuickMessage("some text operationsetupkey")
    if event == 'About':
        sg.PopupQuickMessage("The OICO MST was developed and made by Ophthalmic Instrument Company www.oico.co.uk")
    if event == 'Capture Image':
        sg.Popup('capture image')
window.Close()
