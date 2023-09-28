import base64

def genKeyPass(username, password):
    enc_blob = base64.b64encode(username.encode('utf-8') + b'::' + password.encode('utf-8'))
    return enc_blob