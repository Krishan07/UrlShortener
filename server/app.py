# hashing encoder-decoder (base62 to 10 and back again)
# mongo = dictionary for now
# homepage function (get/post)
# redirect from short url to long url
# get on homepage prints all short and long urls in database (print key, value)
# post generates a hash (encoding functions) saves relation to db, returns shortened url
# use requests to test
# how to validate json
# https://www.google.com/search?channel=fs&client=ubuntu&q=url+shortener+python+flask
# https://impythonist.wordpress.com/2015/10/31/building-your-own-url-shortening-service-with-python-and-flask/
# https://flask.palletsprojects.com/en/2.0.x/
# https://stackoverflow.com/questions/1119722/base-62-conversion


from pymongo import MongoClient
import sys
from flask import Flask, request, redirect, abort
import requests
import hashids

hasher = hashids.Hashids(min_length=5, salt="randomsaltstringfordev")
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
app = Flask(__name__)
max_slink_len = 7
client = MongoClient('localhost', 27017)
db = client['database']
collection = db['collection']


def encode(url):
    return hasher.encode(url)


@app.route('/<path:path>', methods=['GET'])
def path_redirect(path):
    entry = collection.find_one({"new_url": path})
    if entry is not None:
        return redirect(entry['url'], 302)
    else:
        return abort(404)


def url_present(shorturl: str, longurl: str) -> bool:
    return bool(collection.find_one({"new_url": shorturl, 'url': longurl}))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        payload = request.get_json()
        print(payload)
        if 'url' in payload.keys():

            longurl = payload['url']
            state = requests.get(longurl)
            if state.status_code != 200:
                print(state.status_code)
                return {"error": "malformed url"}, 400
            if not longurl.startswith("https://") and not longurl.startswith("http://"):
                longurl = "https://" + longurl
            byte_array = bytearray(longurl, "utf8")
            n = int.from_bytes(byte_array, sys.byteorder)
            shorturl = encode(n)
            print(f"urlis {shorturl}")
            if not url_present(shorturl, longurl):
                collection.insert_one({'new_url': shorturl, 'url': longurl})
            return {'new_url': shorturl, 'url': longurl}
        return {"error": "no url"}, 400
    if request.method == 'GET':
        return {'key': [{'new_url': i['new_url'], 'url': i['url']} for i in collection.find()]}
    return {"error": "only accepts GET/POST"}, 400


if __name__ == "__main__":
    app.run(debug=True)
