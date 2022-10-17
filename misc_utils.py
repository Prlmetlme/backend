import base64

def id_generator():
    from base64 import b32encode
    from hashlib import sha1
    from random import random
    item_id = b32encode(sha1(str(random()).encode('utf-8')).digest()).decode('utf-8')
    item_id = b32encode(sha1(str(random()).encode('utf-8')).digest()).decode('utf-8')
    return str(f'{item_id[0:8]}-{item_id[8:16]}-{item_id[16:24]}-{item_id[24:32]}')

def upload_image(instance, filename):
    return 'images/{filename}'.format(filename=filename)

def url_encode_token(token:str):
    bytes_token = token.encode('ascii')
    encoded_token = base64.urlsafe_b64encode(bytes_token)
    return encoded_token

def url_decode_token(encoded_token):
    bytes_token = base64.urlsafe_b64decode(encoded_token)
    decoded_token = bytes_token.decode('ascii')
    return decoded_token