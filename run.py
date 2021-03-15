import os
import base64
import hashlib

from TwitterAPI import TwitterAPI
import requests

consumer_key = os.getenv('CONSUMER_KEY')
assert isinstance(consumer_key, str)
consumer_secret = os.getenv('CONSUMER_SECRET')
assert isinstance(consumer_secret, str)
key = os.getenv('KEY')
assert isinstance(key, str)
secret = os.getenv('SECRET')
assert isinstance(secret, str)
proxy = os.getenv('https_proxy')
email = os.getenv('EMAIL')
path = os.getenv('IMAGE_PATH')
assert isinstance(email, str) or isinstance(path, str)


def get_gravatar(email: str):
    email = email.strip().lower()
    uid = hashlib.md5(email.encode()).hexdigest()
    url = f'https://www.gravatar.com/avatar/{uid}?s=400&d=retro'
    return requests.get(url).content


if path:
    with open(path, 'rb') as f:
        image = f.read
else:
    image = get_gravatar(email)

api = TwitterAPI(consumer_key, consumer_secret, key, secret, proxy_url=proxy)
res = api.request('account/update_profile_image', {'image': base64.b64encode(image)})

if res.status_code != 200:
    print(f'Failed with status code {res.status_code}')
else:
    print('OK')
