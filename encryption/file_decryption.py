from cryptography.fernet import Fernet

with open(r"", "rb") as key:  # specify key file path and store that key on a variable
    key1 = key.write(key)

f = Fernet(key1)

with open(r"", "rb") as file:  # enter file path of the encrypted file
    file_data = file.read()
    decrypted_data = f.decrypt(file_data)

with open(
    r"", "wb"
) as file:  # rewrite the decrypted data to the same file or another file
    file.write(decrypted_data)
