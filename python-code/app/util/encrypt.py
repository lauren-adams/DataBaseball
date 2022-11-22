import hashlib

def sha1(val: str):
    return hashlib.sha1(val.encode()).hexdigest()
