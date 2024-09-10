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

global movecounter
movecounter = 0

input_log = [] #[x, y, time, key that was pressed, Pressed? (or released[False])]
log_clean = []


global running
running  = True
global start 
start = time.time()

def on_press(key):
    if isinstance(key, str):
        print("string found")
    input_log.append([0, 0, time.time()-start, jsonpickle.encode(key), True, 'kp'])
    log_clean.append([0, 0, str(key), True])
    print("Key pressed: {0}".format(key))
    if key == Key.caps_lock:
        input_log.append(['stop', 'stop', 'stop', 'stop'])
        log_clean.append(['stop', 'stop', 'stop', 'stop'])
        globals()['running'] = False
        return False

def on_release(key):
    input_log.append([0, 0, time.time()-start, jsonpickle.encode(key), False, 'kr'])
    log_clean.append([0, 0, str(key), False])
    print("Key released: {0}".format(key))

def on_move(x, y):
    #if movecounter % 5 == 0:
    #    snapshot = ImageGrab.grab(bbox=(0, 0, 500, 500))
    globals()['movecounter'] += 1

    globals()['curtime'] = time.time()
    input_log.append([x, y, time.time()-start, "moved", False, 'mv'])
    print("Mouse moved to ({0}, {1})".format(x, y))
    return running 

def on_click(x, y, button, pressed):
    if pressed:

        input_log.append([x, y, time.time()-start, jsonpickle.encode(button), True, 'mc'])
        log_clean.append([x, y, str(button), True])
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        input_log.append([x, y, time.time()-start, jsonpickle.encode(button), False, 'mr'])
        log_clean.append([x, y, str(button), False])
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))
    return running

def on_scroll(x, y, dx, dy):
    print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    return running


# Setup the listener threads
keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

# Start the threads and join them so the script doesn't end early
offset = time.time()-start
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()




final = []
inds = 0
for event in input_log:
    if event[0] == "stop":
        break
    event[2] -= offset
    if event[5] == 'mv':
        if inds%20 == 0:
            final.append(event)
        inds += 1
    
    else:
        inds = 0
        final.append(event)

with open('eventlist', 'w') as filehandle:
    json.dump(final, filehandle)

#with open('cleanlist', 'w') as filehandle:
#    json.dump(log_clean, filehandle)



print('start?')
input()

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

            

