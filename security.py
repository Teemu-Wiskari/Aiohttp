from hashlib import md5

from bcrypt import hashpw, checkpw, gensalt


def md5_hash_password(password: str) -> str:
    password: bytes = password.encode()
    hashed_password = md5(password).hexdigest()
    return hashed_password


def bcrypt_hash_password(password: str) -> str:
    password = hashpw(password=password.encode(),
                      salt=gensalt()
                      ).decode()
    return password
