import requests

import requests

url = 'http://localhost:5000'
myobj = {'url': 'https://reddit.com/r/all'}

x = requests.post(url, json=myobj)

print(x.text)


newurl = x.json()["new_url"]
url += "/" + newurl

print(url)

x = requests.get(url)

print(x.text)