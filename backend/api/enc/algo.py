import base64
from cryptography.fernet import Fernet
import hashlib
from django.conf import settings
import os

def genToken(username, password):
    token=hashlib.sha256(username.encode('utf-8') + b'::' + password.encode('utf-8')).digest()
    token=base64.urlsafe_b64encode(token).decode()
    print(token)
    return token

def genFernetKey(token):
    key=bytes(token,'utf-8')
    return key

def genKeyPass(username, password):
    token=genToken(username, password)
    print(token)
    enc_blob = genFernetKey(token)
    secret_token=genToken(settings.SECRET_KEY,"")
    key=genFernetKey(secret_token)
    f=Fernet(key)
    enc_blob = f.encrypt(enc_blob)
    return enc_blob

def verifyKeyPass(enc_blob):
    secret_token=genToken(settings.SECRET_KEY,"")
    key=genFernetKey(secret_token)
    f=Fernet(key)
    try:    
        dec_blob = f.decrypt(enc_blob)
        test=Fernet(dec_blob)
        return True
    except:
        return False

def decryptKeyPass(enc_blob):
    secret_token=genToken(settings.SECRET_KEY,"")
    key=genFernetKey(secret_token)
    f=Fernet(key)
    dec_blob = f.decrypt(enc_blob)
    # token=base64.urlsafe_b64decode(dec_blob)
    return dec_blob.decode('utf-8')
    

def encryptPass(username, password):
    key=genFernetKey(username)
    print("fernet")
    print(key)
    f=Fernet(key)
    token = f.encrypt(password.encode('utf-8'))
    return token


def decryptPass(username, token):
    key=genFernetKey(username)
    f=Fernet(key)
    print(token)
    password = f.decrypt(token)
    return password.decode('utf-8')


def encryptFile(username, filename, encrypted_filename):
    print(filename)
    key=genFernetKey(username)
    f=Fernet(key)
    # settings.BASE_DIR=D:\Documents\GitHub\backend we want file_path=D:\Documents\GitHub\backend\files\files\filename
    file_path=os.path.join(settings.BASE_DIR_ABSOLUTE,'files','files', filename)
    encrypted_file_path=os.path.join(settings.BASE_DIR_ABSOLUTE,'files','files', encrypted_filename)
    print(file_path)
    print(encrypted_file_path)
    with open(file_path, 'rb') as file:
        file_data = file.read()
        file_data = f.encrypt(file_data)
    with open(encrypted_file_path, 'wb') as file:
        file.write(file_data)


def decryptFile(file_data, username):
    key=genFernetKey(username)
    f=Fernet(key)
    decrypted_file_data = f.decrypt(file_data)
    return decrypted_file_data
        