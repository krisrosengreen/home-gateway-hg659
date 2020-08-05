from base64 import b64decode, b64encode
from hashlib import sha256

def encrSha256(text):
    m = sha256()

    m.update(text.encode())

    return m.hexdigest()

def encrBase64(text):
    return b64encode(text.encode()).decode()

def getPassToken(user,passw,param,token):
    b = user + encrBase64(encrSha256(passw)) + param + token;
    passc = encrSha256(b);

    return passc