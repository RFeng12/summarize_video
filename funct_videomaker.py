from flask import Flask, request
from flask import render_template
import requests
import time
import json
import jsonpickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from torch.nn.functional import softmax
from transformers import BertForNextSentencePrediction, BertTokenizer
from gtts import gTTS
import funct_paragrapher
import funct_keyworder
import funct_image_getter
from mutagen.mp3 import MP3
from PIL import Image
from bing_image_urls import bing_image_urls


import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg@5/5.1.6/bin/ffmpeg"


import imageio

from moviepy import editor
from pathlib import Path
import os
from moviepy.editor import *
import os
from natsort import natsorted
import os, shutil
import funct_concat
import numpy as np
from pydub import AudioSegment
import pydub
from moviepy.editor import concatenate_audioclips, AudioFileClip
from PIL import Image, ImageFont, ImageDraw
import re

filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line


im_size = (800, 450)

#string = '''
#    My choice for the greatest invention of the past two thousand years is the lens. I’m going to start, however, with plain old eyeglasses. We don’t really know when they first began to be used. By 1600 there were specialized artisans who carefully ground lenses. One of them, a Dutch eyeglasses maker named Lippershey, noticed that a combination of two lenses made distant objects appear bigger. He tried to use this discovery to get rich. He didn’t succeed, but several of his two-lens devices were made. By 1609 one of them had reached a transplanted Florentine named Galileo Galilei. He pointed his device—or telescope, as it was later called—at the night sky and looked out. What he saw changed our view of the world. The sun rotated around its axis, Venus revolved around the sun, the moon had mountains and valleys, and the Milky Way was made up of vast numbers of stars. It was crystal clear that the old Ptolemaic version of the universe was wrong. The earth was not the center of the universe, and there was no going back. We were launched on our exploration of outer space.
#It is a short journey from the telescope to the microscope. Not surprisingly, they were discovered at around the same time. After all, they are both just the simple piecing together of the right two lenses in correct positions. The microscope, however, was a tool in search of a problem. The problem eventually did develop, and it was nothing less than understanding the origins of life. In 1678 Anton van Leeuwenhoek made a lens good enough to get a magnifying power close to 500. At that point, a whole rich substructure was revealed. A drop of pond water turned out to be filled with little “animalcules” swimming in it. Van Leeuwenhoek had discovered bacteria.
    
#      '''

def write_source(img_path, caption):
    I=Image.open(filepath + img_path)

    Im = ImageDraw.Draw(I)

    Im.text((0, 0), caption,fill=(0, 0, 0))

    I.save(filepath + img_path)

def concatenate_audio_moviepy(audio_clip_paths, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)


def make_video(string, whatis):

    folder = filepath + 'static'
    for filename in sorted(os.listdir(folder)):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    output_coded = funct_paragrapher.get_paragraphs(string)
    output = []
    output_raw = []
    for outputind in range(0, len(output_coded)):
        output_raw.append(output_coded[outputind].replace('S3k22ldkjl9857l', ''))
        output.append(output_coded[outputind].replace('S3k22ldkjl9857l', '...'))
        

    keywords = []
    save = ""
    for outputind in range(0, len(output)):
        paragraph = output[outputind]
        paragraph_raw = output_raw[outputind]

        if outputind %2 == 0:
            save = paragraph_raw
        else:
            print(save + ' ' + paragraph_raw)
            to_search = funct_keyworder.get_keyword_string(save + ' ' + paragraph_raw)
            print("to_search: ", to_search)

            keywords.append(to_search)
            keywords.append(to_search)
            save = ""
    
    if save != "":
        to_search = funct_keyworder.get_keyword_string(output_raw[len(output_raw)-1] + ' ' + save)
        print("to_search: ", to_search)

        keywords.append(to_search)
    




    ind = 0
    first = True



    unfiltered_urls = []

    for i in range(0, 15):
        time.sleep(3)
        try:
            unfiltered_urls = bing_image_urls(whatis, limit=len(output)*12)
        except Exception:
            continue
        if len(unfiltered_urls) > 0:
            break

    interval_len = int((len(unfiltered_urls)-len(output))/len(output))

    for outputind in range(0, len(output)):
        paragraph = output[outputind]
        paragraph_raw = output_raw[outputind]
        myobj = gTTS(text=paragraph, lang='en', slow=False)
        #filename = filepath + "audio_folder/" + str(ind) + '.mp3'
        #myobj.save(filename)
        myobj.save(filepath + "tempaudio.mp3")

        concatenate_audio_moviepy([ filepath+"tempaudio.mp3", filepath + "1sec_silence.mp3"], filepath + "audios.mp3")


        to_search = keywords[outputind]
        if outputind %2 == 0:
            first = True
        else:
            first = False



        ind2 = 0
        # lsdjfldsjlksdjlfjdslkfjldsfjldksfj
        # dlskjflksjflsdjlfkdklsdjlfjslkdsjfs
        #slkdf lkdsjflsd lkfsd klf jsdfl jsdlfjlkds fjlsd
        # sdfkjslkfjdslkjfkldsjlksd
        
        time.sleep(3)



        funct_image_getter.download_images(unfiltered_urls[outputind*interval_len:(outputind+1)*interval_len], 4, 0, paragraph, first, im_size)
    


        oldpwd = os.getcwd()

        audio_path = os.path.join(os.getcwd(), filepath + "audios.mp3")
        video_path = os.path.join(os.getcwd(), filepath + "video_folder")
        images_path = os.path.join(os.getcwd(), filepath + "image_folder")

        audio = MP3(audio_path)
        audio_length = audio.info.length

        print(str(paragraph))

        list_of_images = []
        for image_file in sorted(os.listdir(images_path)):
            print(image_file)
            if image_file.endswith('.png') or image_file.endswith('.jpg'):
                try:
                    image_path = os.path.join(images_path,image_file)
                    image = Image.open(image_path).resize((im_size[0], im_size[1]), Image.Resampling.LANCZOS)
                    
                    arr = np.array(image)

               #     print(arr.shape)
                    if arr.shape == (im_size[1], im_size[0], 3):
                        list_of_images.append(image)
                except Exception:
                    continue
        print(list_of_images)
        print("IMAGE LIST LENGTH", len(list_of_images))
        duration = audio_length/len(list_of_images)





        folder = filepath + 'image_folder'

        for filename in sorted(os.listdir(folder)):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))



        time.sleep(3)



        imageio.mimsave(filepath + 'images.gif', list_of_images, duration=(1000*audio_length/len(list_of_images)))

        video = editor.VideoFileClip(filepath + "images.gif")
        audio = editor.AudioFileClip(audio_path)
        final_video = video.set_audio(audio)


    #    final_video.preview(fps=60)



        os.chdir(video_path)
        final_video.write_videofile(fps=60, codec="libx264", filename=filepath + 'video_' + str(ind) + ".mp4")
        
        os.chdir(oldpwd)

        

        ind += 1


    paths = []
    for i in range(0, ind):
        paths.append(filepath + "video_folder/video_" + str(i) + '.mp4')

    funct_concat.concatenate(paths, filepath + 'static/output.mp4')





    
    folder = filepath + 'video_folder'
    for filename in sorted(os.listdir(folder)):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
            

    folder = filepath + 'simple_images'
    for filename in sorted(os.listdir(folder)):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return 0