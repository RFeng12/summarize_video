

key = "sk-i4HV3B69FYtMdi_EZ9cppaBG2aGFqVRakZsL1KYs9pT3BlbkFJcpcisdB9JDxoRV_VQkZtrx5kBj86Kc3mhnDK-Zp0sA"
from openai import OpenAI
import json
import requests
client = OpenAI(api_key=key)

animal_list = []
with open("vid_topics.txt") as file:
    for line in file.readlines():
        animal_list.append(line.replace('\n', ''))

print(animal_list)

parenthetical = "(animal)"

skip_first = False

import funct_videomaker
import shutil


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

pyautogui.FAILSAFE = False

import jsonpickle

windowsize = pyautogui.size()

from pynput.keyboard import Key, Controller

keyboard = Controller()

from pynput.mouse import Button, Controller

mouse = Controller()




for animal_name in animal_list:
    #try:


        if not skip_first:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": 'write a paragraph answering the question: "what is a ' + animal_name + parenthetical + '?"',
                    }
                ],
                model="gpt-3.5-turbo-0125",
                max_tokens = 450
            )

            video_string = chat_completion.choices[0].message.content

            
            funct_videomaker.make_video(video_string.replace("123 -1..43gg3", "?"), animal_name)

        skip_first = False

        with open('eventlist1') as filehandle:
            final = json.load(filehandle)



        


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

        aoran = ""
        if animal_name[0] in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
            aoran = "an"
        else:
            aoran = 'a'

        
        for char in aoran + ' ' + animal_name:
            if char == ' ':
                keyboard.press(Key.space)

            else:
                keyboard.press(char)

            time.sleep(0.1)


        start += 5


        with open('eventlist2') as filehandle:
            final = json.load(filehandle)


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

        time.sleep(30)
        pyautogui.moveTo(1, 1, duration = 0)
        time.sleep(30)
        pyautogui.moveTo(1, 1, duration = 0)



        


            

   # except Exception:
    #    continue