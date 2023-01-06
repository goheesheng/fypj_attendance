import time, pyautogui, multiprocessing
import PySimpleGUI as sg

def KeepUI():
    sg.theme('Dark')
    layout = [
        [sg.Text('Keep-Me-Up is now running.\nYou can keep it minised, and it will continue running.\nClose it to disable it.')]
    ]
    window = sg.Window('Keep-Me-Up', layout)
    
    p2 = multiprocessing.Process(target = dontsleep)
    p2.start()
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            if p2.is_alive(): 
                p2.terminate()
            break

def dontsleep():
    while True:
        pyautogui.press('volumedown')
        time.sleep(1)
        pyautogui.press('volumeup')
        time.sleep(300)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target = KeepUI)
    p1.start()