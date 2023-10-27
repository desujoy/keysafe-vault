import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib
from django.conf import settings
import os


def genToken(username, password):
    token = hashlib.sha256(
        username.encode("utf-8") + b"::" + password.encode("utf-8")
    ).digest()
    token = base64.urlsafe_b64encode(token).decode()
    print(f"inside gentoken: token={token}")
    return token


def genIV(username):
    iv = hashlib.md5(str.encode(username))
    return iv.digest()


def returnBytes(token):
    key = bytes(token, "utf-8")
    return key


def genKeyPass(username, password):
    token = genToken(username, password)
    print(f"inside genkeypass func token={token}")
    enc_blob = returnBytes(token)
    secret_token = genToken(settings.SECRET_KEY, "")
    print(f"inside genkeypass func secret_token={secret_token}")
    key = returnBytes(secret_token)
    f = Fernet(key)
    enc_blob = f.encrypt(enc_blob)
    return enc_blob


def verifyKeyPass(enc_blob):
    secret_token = genToken(settings.SECRET_KEY, "")
    print(f"inside verifykeypass func secret_token={secret_token}")
    key = returnBytes(secret_token)
    f = Fernet(key)
    try:
        dec_blob = f.decrypt(enc_blob)
        test = Fernet(dec_blob)
        return True
    except:
        return False


def decryptKeyPass(enc_blob):
    secret_token = genToken(settings.SECRET_KEY, "")
    print(f"inside decryptkeypass func secret_token={secret_token}")
    key = returnBytes(secret_token)
    f = Fernet(key)
    dec_blob = f.decrypt(enc_blob)
    # token=base64.urlsafe_b64decode(dec_blob)
    return dec_blob.decode("utf-8")


def encryptPass(username, password):
    key = returnBytes(username)
    print(f"encrypting pass... by {username}")
    f = Fernet(key)
    token = f.encrypt(password.encode("utf-8"))
    return token


def decryptPass(username, token):
    key = returnBytes(username)
    print(f"decrypting pass... by {username}")
    f = Fernet(key)
    # print(token)
    password = f.decrypt(token)
    return password.decode("utf-8")


def encryptFile(username, filename, encrypted_filename):
    print(filename)
    key = returnBytes(username)
    print(f"encrypting file... by {username}")
    f = Fernet(key)
    # settings.BASE_DIR=D:\Documents\GitHub\backend we want file_path=D:\Documents\GitHub\backend\files\files\filename
    file_path = os.path.join(settings.BASE_DIR_ABSOLUTE, "files", "files", filename)
    encrypted_file_path = os.path.join(
        settings.BASE_DIR_ABSOLUTE, "files", "files", encrypted_filename
    )
    print(file_path)
    print(encrypted_file_path)
    with open(file_path, "rb") as file:
        file_data = file.read()
        file_data = f.encrypt(file_data)
    with open(encrypted_file_path, "wb") as file:
        file.write(file_data)


def decryptFile(file_data, username):
    key = returnBytes(username)
    print(f"decrypting file... by {username}")
    f = Fernet(key)
    decrypted_file_data = f.decrypt(file_data)
    return decrypted_file_data


def encryptFile2(username, filename, encrypted_filename):
    print(f"encrypting file 2... by {username}")
    key = base64.urlsafe_b64decode(username)
    iv = genIV(username)
    padder = padding.PKCS7(128).padder()
    a = os.path.join(settings.BASE_DIR_ABSOLUTE, "files", "files", filename)
    with open(a, "rb") as file:
        data1 = file.read()
    data1 = base64.encodebytes(data1)
    padded_data = padder.update(data1)
    padded_data += padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    ct = ct.hex()
    os.remove(a)
    b = os.path.join(settings.BASE_DIR_ABSOLUTE, "files", "files", encrypted_filename)
    with open(b, "wb") as file:
        file.write(ct.encode("utf-8"))


def decryptFile2(file_data, username):
    print(f"decrypting file 2... by {username}")
    unpadder = padding.PKCS7(128).unpadder()
    key = base64.urlsafe_b64decode(username)
    iv = genIV(username)
    data1 = file_data
    data1 = data1.decode("utf-8")
    # print(data1)
    data1 = bytes.fromhex(data1)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    ct = decryptor.update(data1) + decryptor.finalize()
    unpadded_data = unpadder.update(ct)
    unpadded_data += unpadder.finalize()
    unpadded_data = base64.decodebytes(unpadded_data)
    return unpadded_data


def reencryptFile2(old_token, new_token, encrypted_filename):
    a = os.path.join(settings.BASE_DIR_ABSOLUTE,'files','files', encrypted_filename)
    with open(a, "rb") as file:
        data1 = file.read()
    decrpted_data1=decryptFile2(data1, old_token)
    with open(a, "wb") as file:
        file.write(decrpted_data1)
    encryptFile2(new_token,encrypted_filename,encrypted_filename)

# def reencryptFile2(old_token, new_token, encrypted_filename):
#     print(f"decrypting file 2... by {old_token}")
#     old_key = base64.urlsafe_b64decode(old_token)
#     old_iv = genIV(old_token)
#     unpadder = padding.PKCS7(128).unpadder()
#     a = os.path.join(settings.BASE_DIR_ABSOLUTE, "files", "files", encrypted_filename)
#     with open(a, "rb") as file:
#         data1 = file.read()
#     data1 = data1.decode("utf-8")
#     data1 = bytes.fromhex(data1)
#     cipher = Cipher(algorithms.AES(old_key), modes.CBC(old_iv))
#     decryptor = cipher.decryptor()
#     ct = decryptor.update(data1) + decryptor.finalize()
#     unpadded_data = unpadder.update(ct)
#     unpadded_data += unpadder.finalize()
#     unpadded_data = base64.decodebytes(unpadded_data)
#     print(f"encrypting file 2... by {new_token}")
#     new_key = base64.urlsafe_b64decode(new_token)
#     new_iv = genIV(new_token)
#     padder = padding.PKCS7(128).padder()
#     padded_data = padder.update(unpadded_data)
#     padded_data += padder.finalize()
#     cipher = Cipher(algorithms.AES(new_key), modes.CBC(new_iv))
#     encryptor = cipher.encryptor()
#     ct = encryptor.update(padded_data) + encryptor.finalize()
#     ct = ct.hex()
#     with open(a, "wb") as file:
#         file.write(ct.encode("utf-8"))
    