import os
from pathlib import Path
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.config_path = Path("config/.env")
        
    def encrypt_value(self, value: str) -> bytes:
        return self.cipher_suite.encrypt(value.encode())
        
    def decrypt_value(self, encrypted_value: bytes) -> str:
        return self.cipher_suite.decrypt(encrypted_value).decode()
        
    def store_api_key(self, service: str, api_key: str):
        encrypted_key = self.encrypt_value(api_key)
        os.environ[f"{service.upper()}_API_KEY"] = encrypted_key.decode()
        
    def get_api_key(self, service: str) -> str:
        encrypted_key = os.environ.get(f"{service.upper()}_API_KEY")
        if encrypted_key:
            return self.decrypt_value(encrypted_key.encode())
        return None
