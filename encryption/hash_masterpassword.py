import bcrypt
from cryptography.fernet import Fernet

username = b"johndoe"  # username and password input should be in a byte string
password = b"password123"
string_to_be_hashed = (
    username + password
)  # create a concatenated byte string of username and password
print("string to be hashed : ", string_to_be_hashed)
salt = bcrypt.gensalt(rounds=12)
print("salt : ", salt)
with open(r"salt.txt", "wb") as salting:  # generate salt and store it in a file
    salting.write(salt)
hashed_password = bcrypt.hashpw(string_to_be_hashed, salt)

key = Fernet.generate_key()
f = Fernet(key)
with open(
    r"master_pass_enc_key.key", "wb"
) as keyenc:  # store master password encryption key to a .key file and send it to the user if required later for recovery
    keyenc.write(key)
encrypted_master_password = f.encrypt(hashed_password)

with open(r"hashed_password.key", "wb") as hashpass:  # store hashed password
    hashpass.write(hashed_password)

print("encrypted master password : ", encrypted_master_password)

with open(
    r"encrypted_master_password.key", "wb"
) as psswd:  # store encrypted master password
    psswd.write(encrypted_master_password)
