import pyautogui
import time
import json

#idea: reading the text on the page to determine if you're at the same stage
from pynput import mouse
from pynput.keyboard import Key

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from PIL import ImageGrab
import pyautogui
import jsonpickle

windowsize = pyautogui.size()

from pynput.keyboard import Key, Controller

keyboard = Controller()

from pynput.mouse import Button, Controller

mouse = Controller()


with open('eventlist') as filehandle:
    final = json.load(filehandle)

print(len(final))




start = time.time()+5

for event in final:
#    print(event)
    while True:
        if time.time()-start >= event[2]:
            break

    print("Time: ", time.time()-start, ', eventime: ', event[2])

    if event[5] == 'kp' or event[5] == 'kr':
        if event[4]:
            keyboard.press(jsonpickle.decode(event[3]))

        else:
            keyboard.release(jsonpickle.decode(event[3]))

    else: 
        if event[5] == 'mv':
            pyautogui.moveTo(event[0], event[1], duration = 0)
        if event[5] == 'mc':
            pyautogui.moveTo(event[0], event[1], duration = 0)
            mouse.press(jsonpickle.decode(event[3]))
        if event[5] == 'mr':
            pyautogui.moveTo(event[0], event[1], duration = 0)
            mouse.release(jsonpickle.decode(event[3]))

            

