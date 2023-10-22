import base64
from cryptography.fernet import Fernet
import hashlib
from django.conf import settings

def genFernetKey(username):
    blob=hashlib.sha256(username.encode()).digest()
    key=base64.urlsafe_b64encode(blob)
    return key

def genKeyPass(username, password):
    enc_blob = base64.b64encode(username.encode('utf-8') + b'::' + password.encode('utf-8'))
    key=genFernetKey(settings.SECRET_KEY)
    f=Fernet(key)
    enc_blob = f.encrypt(enc_blob)
    return enc_blob

def verifyKeyPass(username, password, enc_blob):
    key=genFernetKey(settings.SECRET_KEY)
    f=Fernet(key)
    dec_blob = f.decrypt(enc_blob)
    username, password = dec_blob.decode('utf-8').split('::')
    if username == username and password == password:
        return True
    else:
        return False

def encryptPass(username, password):
    key=genFernetKey(username)
    f=Fernet(key)
    token = f.encrypt(password.encode('utf-8'))
    return token

def decryptPass(username, token):
    key=genFernetKey(username)
    f=Fernet(key)
    print(token)
    password = f.decrypt(token)
    return password.decode('utf-8')