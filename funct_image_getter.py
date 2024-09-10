from simple_image_download import simple_image_download as simp
import re
import requests
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from bing_image_urls import bing_image_urls
import time
import os
import imageio


key="AIzaSyAWlxkryGfobU0DsdXh5CEAzlvAArHCvGI"


filepath = ""
with open("filepath.txt") as file:
    for line in file.readlines():
        filepath = line

font = ImageFont.truetype(r'/Users/rfeng12/Library/CloudStorage/OneDrive-Personal/Desktop/summarize_video/arial.ttf', 16)
fontsmall = ImageFont.truetype(r'/Users/rfeng12/Library/CloudStorage/OneDrive-Personal/Desktop/summarize_video/arial.ttf', 10)

timeoutsec = 25

def write_source(img_path, caption, x, y, charline, font):
    I=Image.open(filepath + img_path)

    Im = ImageDraw.Draw(I)


    charsperline = charline

    tempinput = ""
    paragraph = caption
    for word in paragraph.split(' '):
        if len(tempinput) + len(word) > charsperline:
            Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")
            Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")
            Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")
            Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")

            Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255), font=font, align="center")
            tempinput = ""
            y += 15
        tempinput += ' ' + word

    Im.text((x+1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")
    Im.text((x+1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")
    Im.text((x-1, y+1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")
    Im.text((x-1, y-1), str(tempinput).encode('cp1252'),fill=(0, 0, 0), font=font, align="center")

    Im.text((x, y), str(tempinput).encode('cp1252'),fill=(255, 255, 255), font=font, align="center")

    I.save(filepath + img_path)



def download_images(keywords, num, index, paragraph, outputslice, im_size):


    unfiltered_urls = keywords



    url_list = []
    
    for unfiltered in unfiltered_urls:
        if unfiltered[-4:] == '.jpg':
            url_list.append(unfiltered)


    print(len(url_list))


    if len(url_list) == 0 or keywords == "noimagefound":
        for i in range(0, num):
            with open('widelogo.jpg', 'rb') as fd:
                img_data = fd.read()
            with open(filepath + 'image_folder/' + str(index) + str(i) + '.jpg', 'wb') as handler:
                handler.write(img_data)

            image_path = filepath + 'image_folder/' + str(index) + str(i) +  '.jpg'
            source = ''
            image = Image.open(image_path).convert("RGB").resize((im_size[0], im_size[1]), Image.Resampling.LANCZOS)
            
            image.save(image_path)

            write_source(image_path, paragraph, 20, im_size[1]-100, 90, font)

            write_source(image_path, source, 0, 0, 120, fontsmall)
            
    # url list not 0        
    else:
        ind = 0
        source = ""
        for i in range(0, num):
            if i >= len(url_list):
                if(len(url_list) >= 3):
                    
                    try:
                        img_data = requests.get(url_list[i%len(url_list)], timeout=timeoutsec).content  
                        source = url_list[i%len(url_list)]

                    except Exception:
                        with open('widelogo.jpg', 'rb') as fd:
                            img_data = fd.read()
                        source = ''
                else :

                    with open('widelogo.jpg', 'rb') as fd:
                        img_data = fd.read()
                    source = ''
            else:
                try:
                    img_data = requests.get(url_list[i], timeout=timeoutsec).content
                    source = url_list[i]
                except Exception:
      
                    with open('widelogo.jpg', 'rb') as fd:
                        img_data = fd.read()
                    source = ''
            try:
                with open(filepath + 'image_folder/' +   str(index) + "im" + str(ind) + '.jpg', 'wb') as handler:
                    handler.write(img_data)
                

                image_path = filepath + 'image_folder/' +   str(index) + "im" + str(ind) + '.jpg'
                image_back = Image.open(image_path)
                width, height = image_back.size

                resize_ratio = float(min((im_size[0]-50)/width, (im_size[1]-50)/height))
                image_original = image_back.convert('RGB').resize((int(width*resize_ratio), int(height*resize_ratio)), Image.Resampling.LANCZOS)
                
                resize_ratio = float(max(im_size[0]/width, im_size[1]/height))
                image_back = image_back.convert('RGB').resize((int(width*resize_ratio), int(height*resize_ratio)), Image.Resampling.LANCZOS).filter(ImageFilter.BoxBlur(radius=6))    
                width, height = image_back.size
                image_back = image_back.crop((int((width-im_size[0])/2), int((height-im_size[1])/2), int(width-(width-im_size[0])/2), int(height-(height-im_size[1])/2) ))
                
                owidth, oheight = image_original.size
                Image.Image.paste(image_back, image_original, (int((im_size[0]-owidth)/2), int((im_size[1]-oheight)/2)))
                width, height = image_back.size

                #   print(width, ' ', height)

                image_back.save(image_path)

                write_source(image_path, paragraph, 20, im_size[1]-100, 90, font)

                write_source(image_path, source, 0, 0, 120, fontsmall)


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