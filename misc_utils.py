def id_generator():
    from base64 import b32encode
    from hashlib import sha1
    from random import random
    item_id = b32encode(sha1(str(random()).encode('utf-8')).digest()).decode('utf-8')
    item_id = b32encode(sha1(str(random()).encode('utf-8')).digest()).decode('utf-8')
    return str(f'{item_id[0:8]}-{item_id[8:16]}-{item_id[16:24]}-{item_id[24:32]}')

def upload_image(instance, filename):
    return 'images/{filename}'.format(filename=filename)