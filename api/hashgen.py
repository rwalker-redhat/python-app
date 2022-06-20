import hashlib
import os
import random
import string

import fastapi

router = fastapi.APIRouter()


@router.get('/api/hashgen')
def hashgen():
    salt = os.urandom(1024)
    letters = string.ascii_lowercase
    random_letters = (''.join(random.choice(letters) for i in range(16)))
    key = hashlib.pbkdf2_hmac('sha512', random_letters.encode('utf-8'), salt, 1000000, dklen=128)
    keyhex = str(key.hex())
    return keyhex

