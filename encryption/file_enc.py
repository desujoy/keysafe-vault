import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

key = b'\x8a"SI}\xbc\xe11\x0b\xa4b\xef\xd2\x13z0/\xeb\x8a\xae\xae\x8e\xad\xb3\x8c,\xbe\x1c\xae\x00H\x1e'
iv = b'H\x07z,\xf9\x8dg\xa9\xee\x02\x1a\xa9\x88P\t\xe9'

padder = padding.PKCS7(128).padder()

a = r"C:\Users\HP\OneDrive\Desktop\ee.txt"

with open(a,'rb') as file:
    data1 = file.read()
print(data1)

padded_data = padder.update(data1)
padded_data += padder.finalize()


cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ct = encryptor.update(padded_data) + encryptor.finalize()
ct = ct.hex()

with open(a, 'wb') as file:
    file.write(ct.encode('utf-8'))


