import urllib.request, urllib.parse
import json
import sqlite3
# import ssl

def lookup_item(item_id): 
    base_url = 'https://archive.org/metadata/'
    url = base_url + item_id 
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()

    item_title = ''
    addeddate = ''
    file_name = ''
    file_length = 0

    try:
        js = json.loads(data)
    except:
        js = None
    
    if not js or 'metadata' not in js:
        print('==== Download error ===')
        print(data)

    if len(js['metadata']) == 0:
        print('==== Object not found ====')
        print(data)
        # break

    addeddate = js['metadata']['addeddate']
    # print(addeddate)
    item_title = js['metadata']['title']

    if not js or 'files' not in js:
        print('==== Download error ===')
        print(data)

    if len(js['files']) == 0:
        print('==== Object not found ====')
        print(data)
    
    files = js['files']
    # if there's multiple original video files, it will return whichever is last    
    for file in files: 
        if file['source'] == 'original':
            if 'length' in file: 
                file_length = file['length']
                if 'name' in file: 
                    file_name = file['name']
                else: 
                    print('==== Missing File Name ====')
                    print(file)
                    file_name = ''
    return item_title, addeddate, file_name, file_length

conn = sqlite3.connect('iadb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Videos')

cur.execute('''
CREATE TABLE Videos (item_id TEXT
            , item_title TEXT
            , file_name TEXT
            , file_length INTEGER
            , added_date DATE
            )''')

# insert into SQL database item_id, item_title, file_name, file_length, added_date

serviceurl = 'https://archive.org/advancedsearch.php?output=json&fl%5B%5D=identifier&sort%5B%5D=&rows=100&q='
# query_string = 'mediatype%3A%28movies%29+AND+date%3A2024-06-18'
query_string = 'mediatype%3A%28movies%29+AND+date%3A%5B2024-06-01%20TO%202024-06-18%5D'



url = serviceurl + query_string 

uh = urllib.request.urlopen(url)
data = uh.read().decode()

try:
    js = json.loads(data)
except:
    js = None

if not js or 'response' not in js:
    print('==== Download error ===')
    print(data)
    # break

if len(js['response']) == 0:
    print('==== Object not found ====')
    print(data)
    # break

if len(js['response']['docs']) == 0:
    print('==== Items not found ====')
    print(data)
    # break

numFound = js['response']['numFound']
print('Number Found: ', numFound)
item_counter = 0
page_counter = 1

while item_counter <= numFound:
    page_string = '&page=' + str(page_counter)
    url = serviceurl + query_string + page_string
    # print(url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    docs = js['response']['docs']
    for item in docs: 
        item_counter+=1
        # print('Item',item_counter,item['identifier'])
        item_id = item['identifier']
        item_title, added_date, file_name, file_length = lookup_item(item_id)
        print('Item', item_counter,':', item_id, item_title, added_date, file_name, file_length)
        cur.execute('''INSERT INTO Videos (item_id, item_title, file_name, file_length, added_date)
                VALUES (?, ?, ?, ?, ?)''', (item_id, item_title, file_name, file_length, added_date))
    conn.commit()
    page_counter += 1

# insert into SQL database item_id, item_title, file_name, file_length, added_date