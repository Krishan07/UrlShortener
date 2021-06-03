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
import json
import sys
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, abort
from string import digits, ascii_letters
from secrets import choice
from urllib.parse import urlparse

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
app = Flask(__name__)
max_slink_len = 7
client = MongoClient('localhost', 27017)
db = client['database']
collection = db['collection']


def encode(num, alphabet):
    """Encode a positive number into Base X and return the string.

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(alphabet)
    while num:
        num, rem = _divmod(num, base)
        arr_append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def decode(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for decoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num


@app.route('/<path:path>', methods=['GET'])
def path_redirect(path):
    if path in redirects.keys():
        return redirect(redirects[path], 302)
    else:
        return abort(404)


def url_present(shorturl: str) -> bool:
    return bool(collection.find_one({"new_url": shorturl}))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        payload = request.get_json()  # must figure this out (small url key, big url value)
        print(payload)
        if 'url' in payload.keys():
            # TODO:: validate url + add https:// if it isnt there
            longurl = payload['url']
            byte_array = bytearray(longurl, "utf8")
            n = int.from_bytes(byte_array, sys.byteorder)
            shorturl = encode(n, BASE62)
            if url_present(shorturl):
                collection.insert_one({'newu_rl': shorturl, 'url': longurl})
            return {'new_url': shorturl, 'url': longurl}
            # add something to prevent base62 collision if it occurs
    if request.method == 'GET':
        return json.dumps(list(collection.find()))
    return "FUCKING"


if __name__ == "__main__":
    app.run(debug=True)

temp = encode("thing", BASE62)
print(temp)
print(decode(temp, BASE62))
