## testing out the JSON API for items

import urllib.request, urllib.parse
import json
# import ssl

serviceurl = 'https://archive.org/metadata/'

# # Ignore SSL certificate errors
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

# item_id = '0-.compressed'
# item_id = 'FrankenberryCountChoculaTevevisionCommercial1971'
item_id = '2024.06.11-unarchived-karaoke-27.9-said-they-wanted-an-unarchive-karaoke-kureiji-ollie-video-1080p'

url = serviceurl + item_id 

# print(url)
uh = urllib.request.urlopen(url)
# uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

try:
    js = json.loads(data)
except:
    js = None

if not js or 'metadata' not in js:
    print('==== Download error ===')
    print(data)
    # break

if len(js['metadata']) == 0:
    print('==== Object not found ====')
    print(data)
    # break

addeddate = js['metadata']['addeddate']
# [0]['properties']['plus_code']
print(addeddate)

item_title = js['metadata']['title']


if not js or 'files' not in js:
    print('==== Download error ===')
    print(data)
    # break

if len(js['files']) == 0:
    print('==== Object not found ====')
    print(data)
    # break


files = js['files']

for file in files: 
    if file['source'] == 'original':
        if 'length' in file: 
            file_length = file['length']
            print('length in seconds:', file_length)
            file_name = file['name']
            print(file_name)

# print(js['files'])
