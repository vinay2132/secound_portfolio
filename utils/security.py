"""
Security utilities for handling API key encryption
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SECRET_KEY_FILE = ".secret_key"
SALT_FILE = ".salt"

def generate_key_from_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
    Derive a Fernet key from a password using PBKDF2.
    Returns (key, salt).
    """
    if salt is None:
        salt = os.urandom(16)
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def save_salt(salt: bytes):
    """Save the salt to a file"""
    with open(SALT_FILE, "wb") as f:
        f.write(salt)

def load_salt() -> bytes:
    """Load the salt from file"""
    if not os.path.exists(SALT_FILE):
        return None
    with open(SALT_FILE, "rb") as f:
        return f.read()

def encrypt_api_key(api_key: str, password: str) -> bool:
    """
    Encrypt and save the API key using the password.
    Returns True if successful.
    """
    try:
        key, salt = generate_key_from_password(password)
        f = Fernet(key)
        encrypted_data = f.encrypt(api_key.encode())
        
        # Save salt and encrypted key
        save_salt(salt)
        with open(SECRET_KEY_FILE, "wb") as f:
            f.write(encrypted_data)
        return True
    except Exception as e:
        print(f"Encryption error: {e}")
        return False

def decrypt_api_key(password: str) -> str:
    """
    Decrypt the API key using the password.
    Returns the API key if successful, None otherwise.
    """
    try:
        if not os.path.exists(SECRET_KEY_FILE):
            return None
            
        salt = load_salt()
        if not salt:
            return None
            
        key, _ = generate_key_from_password(password, salt)
        f = Fernet(key)
        
        with open(SECRET_KEY_FILE, "rb") as file:
            encrypted_data = file.read()
            
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode()
    except Exception:
        return None

def is_key_set() -> bool:
    """Check if the encrypted key file exists"""
    return os.path.exists(SECRET_KEY_FILE) and os.path.exists(SALT_FILE)

def clear_key():
    """Remove the stored key and salt"""
    if os.path.exists(SECRET_KEY_FILE):
        os.remove(SECRET_KEY_FILE)
    if os.path.exists(SALT_FILE):
        os.remove(SALT_FILE)
