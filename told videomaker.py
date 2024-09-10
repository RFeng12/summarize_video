from simple_image_download import simple_image_download as simp
import re
import requests
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from bing_image_urls import bing_image_urls
import time
import os
import imageio

filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line


timeoutsec = 25

def write_source(img_path, caption, x, y):
    I=Image.open(filepath + img_path)

    Im = ImageDraw.Draw(I)


    charsperline = 60

    tempinput = ""
    paragraph = caption
    for i, letter in enumerate(paragraph):
        if i % charsperline == 0:
            Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
            Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

            Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))
            tempinput = ""
            y += 15
        tempinput += letter

    Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
    Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
    Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))
    Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0))

    Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255))

    I.save(filepath + img_path)



def download_images(keywords, num, index, paragraph):
    keywords = keywords.replace(" ", "d328749201d")
    keywords = re.sub('[\W_]+', '', keywords)
    keywords = keywords.replace("d328749201d", " ")
    print("searching.. ", keywords)


    unfiltered_urls = []

    for i in range(0, 10):
        time.sleep(0.5)
        try:
            unfiltered_urls = bing_image_urls(keywords.strip(), limit=15)
        except Exception:
            continue
        if len(unfiltered_urls) > 0:
            break


    url_list = []
    
    for unfiltered in unfiltered_urls:
        if unfiltered[-4:] == '.jpg':
            url_list.append(unfiltered)


    print(len(url_list))


    if len(url_list) == 0 or keywords == "noimagefound":
        for i in range(0, num):
            with open('logo.jpg', 'rb') as fd:
                img_data = fd.read()
            with open(filepath + 'image_folder/' + str(index) + str(i) + '.jpg', 'wb') as handler:
                handler.write(img_data)

            image_path = filepath + 'image_folder/' + str(index) + str(i) +  '.jpg'
            source = ''
            image = Image.open(image_path).convert("RGB").resize((400, 400), Image.Resampling.LANCZOS)
            image.save(image_path)

            write_source(image_path, paragraph, 20, 100)

            write_source(image_path, source, 0, 0)
            
    # url list not 0        
    else:
        ind = 0
        source = ""
        for i in range(0, num):
            if i >= len(url_list):
                with open('logo.jpg', 'rb') as fd:
                    img_data = fd.read()
                source = ''
            else:
                try:
                    img_data = requests.get(url_list[i], timeout=timeoutsec).content
                    source = url_list[i]
                except Exception:
                    with open('logo.jpg', 'rb') as fd:
                        img_data = fd.read()
                    source = ''
            try:
                with open(filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + '.jpg', 'wb') as handler:
                    handler.write(img_data)
                

                
                image_path = filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + '.jpg'
                image = Image.open(image_path).convert('RGB').resize((400, 400), Image.Resampling.LANCZOS).filter(ImageFilter.BoxBlur(radius=6))
                image.save(image_path)

                write_source(image_path, paragraph, 20, 100)

                write_source(image_path, source, 0, 0)


            except Exception:
                continue
                '''
                print("EXCEPTION FOUND")
                print("EXCEPTION FOUND")


                with open(filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + 'nif' + '.jpg', 'wb') as handler:
                    img_data = requests.get('https://i.ibb.co/SyF2DWV/No-Image-Available.jpg').content  
                    handler.write(img_data)
                    source = 'https://i.ibb.co/SyF2DWV/No-Image-Available.jpg'
                
                image_path = filepath + 'image_folder/' +   str(index) + keywords.replace(" ", "") + str(ind) + 'nif' + '.jpg'
                image = Image.open(image_path).convert("RGB").resize((400, 400), Image.Resampling.LANCZOS)
                image.save(image_path)

                write_source(image_path, paragraph, 20, 100)

                write_source(image_path, source, 0, 0)
                '''
                
            ind += 1

    my_downloader = simp.simple_image_download()
    my_downloader.extensions = '.jpg'




    return 1

'''
# Change Direcotory
my_downloader.directory = 'my_dir/'
# Change File extension type
my_downloader.extensions = '.jpg'
print(my_downloader.extensions)
my_downloader.download('laptop', limit=10, verbose=True)
'''