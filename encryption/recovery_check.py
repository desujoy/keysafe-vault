from cryptography.fernet import Fernet
import bcrypt

with open(
    r"master_pass_enc_key.key", "rb"
) as mspe:  # file path specified should be a raw string
    master_pass_enc_key = mspe.read()

with open(r"encrypted_master_password.key", "rb") as mspe:
    encrypted_master_password = mspe.read()

with open(r"hashed_password.key", "rb") as mspe:
    hashed_password = mspe.read()

f = Fernet(master_pass_enc_key)
decrypted_master_password_hash = f.decrypt(encrypted_master_password)

if decrypted_master_password_hash == hashed_password:
    print("recovery successful, you will now be redirected to a new page....")
else:
    print("invalid key")
