import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

unpadder = padding.PKCS7(128).unpadder()

key = b'\x8a"SI}\xbc\xe11\x0b\xa4b\xef\xd2\x13z0/\xeb\x8a\xae\xae\x8e\xad\xb3\x8c,\xbe\x1c\xae\x00H\x1e'
iv = b'H\x07z,\xf9\x8dg\xa9\xee\x02\x1a\xa9\x88P\t\xe9'

<<<<<<< HEAD
a = r"cubes.png"
=======
a = r"C:\Users\HP\OneDrive\Desktop\ee.txt"
>>>>>>> d3c80eb9ee9797b26d30de947d906819adace91b

with open(a,'rb') as file:
    data1 = file.read()
print(data1)
data1 = data1.decode("utf-8")
data1 = bytes.fromhex(data1)


cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()
ct = decryptor.update(data1) + decryptor.finalize()

unpadded_data = unpadder.update(ct)
unpadded_data+= unpadder.finalize()

<<<<<<< HEAD
with open(r"cubes1.png", 'wb') as file:
=======
with open(a, 'wb') as file:
>>>>>>> d3c80eb9ee9797b26d30de947d906819adace91b
    file.write(unpadded_data)