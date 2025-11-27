from hashlib import sha256


def sec_password(password_def: str, hash_password: str) -> bool:
    hash_o = sha256(password_def.encode())
    return hash_o.hexdigest() == hash_password


def create_hash(password_def: str):
    hash_o = sha256(password_def.encode())
    return hash_o.hexdigest()

# {
#  "email": "user@gmail.com",
# "password": "strsafing",
# "username": "strifffdsng"
# }
