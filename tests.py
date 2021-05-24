import requests

import requests

url = 'http://localhost:5000'
myobj = {'url': 'https://reddit.com'}

x = requests.post(url, json=myobj)

print(x.json())


newurl = x.json()["newurl"]
url += "/" + newurl

print(url)

x = requests.get(url)

print(x.text)