# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.4 Secure Data Handling

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

class DataEncryption:
    """Encrypt sensitive data."""
    
    def __init__(self, password: str = None):
        if password:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'fixed_salt',  # In production, use random salt
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        else:
            key = Fernet.generate_key()
        
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt data."""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

class SecureResourceHandler:
    """Handle resources with encryption."""
    
    def __init__(self):
        self.encryption = DataEncryption()
        self.classifier = DataClassifier()
    
    def read_resource_securely(self, uri: str) -> str:
        """Read and decrypt resource if needed."""
        # Read resource
        content = self._read_resource(uri)
        
        # Check if encrypted
        if content.startswith("encrypted:"):
            encrypted = content.replace("encrypted:", "")
            return self.encryption.decrypt(encrypted)
        
        return content
    
    def store_resource_securely(self, uri: str, content: str):
        """Store resource with encryption if needed."""
        # Classify data
        classification = self.classifier.classify(content)
        
        # Encrypt if confidential or restricted
        if classification in [DataClassification.CONFIDENTIAL, 
                            DataClassification.RESTRICTED]:
            encrypted = self.encryption.encrypt(content)
            content = f"encrypted:{encrypted}"
        
        # Store resource
        self._store_resource(uri, content)