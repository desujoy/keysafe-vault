from cryptography.fernet import Fernet

key = Fernet.generate_key()

f = Fernet(key)
print(key)
with open(r"", "wb") as key:  # write a .key file to a specific file path
    key.write(key)

with open(r"", "rb") as file:  # path of file whose data is to be encrypted
    file_data = file.read()
    encrypted_data = f.encrypt(file_data)

with open(
    r"", "wb"
) as file:  # rewrite encrypted data of file to the file path or another file
    file.write(encrypted_data)
