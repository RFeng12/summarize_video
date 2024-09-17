import json
import urllib
import requests

url = 'https://parseapi.back4app.com/classes/Animal?limit=100000000000000&keys=name'
headers = {
    'X-Parse-Application-Id': 'J6ak82bJU9kZjue3uPgKyaM4oOhkC1qZXYaGYUck', # This is the fake app's application id
    'X-Parse-Master-Key': 'j9dri8K7xJI3Hv2uEmTteJdq76o4uTYbcGauY6oA' # This is the fake app's readonly master key
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
#print(json.dumps(data, indent=2))
#print(data['results'][0]['name'])
#print(data['results'])

with open('vid_topics.txt', 'w') as f:
    for line in data['results']:
        f.write(line['name'] + '\n')