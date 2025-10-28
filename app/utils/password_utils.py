import bcrypt
import hashlib

def hash_password(password: str) -> str:
    """
    Hash a password safely using SHA256 -> bcrypt.
    Returns the hashed password as a UTF-8 string.
    """
    # Convert password to bytes
    password_bytes = password.encode("utf-8")
    # SHA256 digest (fixed 32 bytes)
    sha256_digest = hashlib.sha256(password_bytes).digest()
    # Generate bcrypt salt
    salt = bcrypt.gensalt()
    # Hash SHA256 digest with bcrypt
    hashed = bcrypt.hashpw(sha256_digest, salt)
    # Return as string
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password using SHA256 -> bcrypt.
    """
    password_bytes = plain_password.encode("utf-8")
    sha256_digest = hashlib.sha256(password_bytes).digest()
    return bcrypt.checkpw(sha256_digest, hashed_password.encode("utf-8"))

