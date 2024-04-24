from passlib.context import CryptContext

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "SHA256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# hashing algo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    new_hashed_pass = get_password_hash(plain_password)
    return new_hashed_pass == hashed_password


def get_password_hash(password):
    a = _hash_password(password)
    return a


def _hash_password(password: str):
    from hashlib import sha256
    return sha256(password.encode('utf-8')).hexdigest()
