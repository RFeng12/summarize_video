#!/usr/bin/python

import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


import json
import urllib
import requests

url = 'https://parseapi.back4app.com/classes/Animal?limit=100000000000000&keys=name'
headers = {
    'X-Parse-Application-Id': 'J6ak82bJU9kZjue3uPgKyaM4oOhkC1qZXYaGYUck', # This is the fake app's application id
    'X-Parse-Master-Key': 'j9dri8K7xJI3Hv2uEmTteJdq76o4uTYbcGauY6oA' # This is the fake app's readonly master key
}
animal_list = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
#print(json.dumps(data, indent=2))
#print(data['results'][0]['name'])


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret_658153319851-g4ibdhd7cu09s5rb8ika01aiqa3u6v9a.apps.googleusercontent.com.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = '''
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
%s
with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
''' % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, opt):
  tags = None
  if opt.keywords:
    tags = opt.keywords.split(",")

  body=dict(
    snippet=dict(
      title=opt.title,
      description=opt.description,
      tags=tags,
      categoryId=opt.category
    ),
    status=dict(
      privacyStatus=opt.privacyStatus
    )
  )

  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    
    media_body=MediaFileUpload(opt.file, chunksize=-1, resumable=True)
  )

  resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print("Video id '%s' was successfully uploaded."% response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)





key = "sk-i4HV3B69FYtMdi_EZ9cppaBG2aGFqVRakZsL1KYs9pT3BlbkFJcpcisdB9JDxoRV_VQkZtrx5kBj86Kc3mhnDK-Zp0sA"
from openai import OpenAI
client = OpenAI(api_key=key)


import funct_videomaker
import shutil

for animal in animal_list['results'][:6]:
    try:
        animal_name = animal['name']

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": 'write a paragraph answering the question: "what is a ' + animal_name + '?"',
                }
            ],
            model="gpt-3.5-turbo-0125",
            max_tokens = 300
        )

        video_string = chat_completion.choices[0].message.content

        funct_videomaker.make_video(video_string.replace("123 -1..43gg3", "?"), animal_name)




        args = argparser.parse_args()
        args.file = "/Users/rfeng12/Library/CloudStorage/OneDrive-Personal/Desktop/summarize_video/static/output.mp4"
        
        aoran = ""
        if animal_name[0] in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
            aoran = "an"
        else:
            aoran = 'a'
        
        
        args.title = "What is " + aoran + ' ' + animal_name
        args.description = "Explain what is " + aoran + ' ' + animal_name
        args.keywords = animal_name
        args.category = "22"
        args.privacyStatus = "public"


        if not os.path.exists(args.file):
            exit("Please specify a valid file using the --file= parameter.")

        youtube = get_authenticated_service(args)
        try:
            initialize_upload(youtube, args)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    except Exception:

        print("EXCEPTION FOUND")
        print("EXCEPTION FOUND")
        print("EXCEPTION FOUND")
        print("EXCEPTION FOUND")
        print("EXCEPTION FOUND")
        print("EXCEPTION FOUND")
        filepath = ""

        folder = filepath + 'image_folder'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


        folder = filepath + 'video_folder'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        folder = filepath + 'simple_images'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        folder = filepath + 'static'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))





