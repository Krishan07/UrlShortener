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


# from pymongo import MongoClient
from os import getenv
from flask import Flask, request, render_template, redirect, url_for, abort
from string import digits, ascii_letters
from secrets import choice
from urllib.parse import urlparse

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
app = Flask(__name__)
max_slink_len = 7
redirects = {
    "shorturl1": "youtube.com",
    "shorturl2": "twitter.com",
    "shorturl3": "reddit.com",
}


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
    redirect_path = redirects.find_one({"path_from": path})

    if not redirect_path:
        return '404'
    else:
        return redirect_path=redirect_path['shorturl1']


@app.route('/')
def home():
    if request.method == 'POST':
        original_url = request.get_json()  # must figure this out
        if urlparse(original_url).scheme == '':
            original_url = 'http://' + original_url

    return "FUCKING"


if __name__ == "__main__":
    app.run(debug=True)

temp = encode(123, BASE62)
print(temp)
print(decode(temp, BASE62))
