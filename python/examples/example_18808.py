# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.2 Protocol Evolution and Roadmap

from cryptography.fernet import Fernet

class EncryptedMCPTransport:
    """MCP transport with end-to-end encryption."""
    
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)
    
    def encrypt_message(self, message: Dict) -> bytes:
        """Encrypt MCP message."""
        message_json = json.dumps(message).encode()
        return self.cipher.encrypt(message_json)
    
    def decrypt_message(self, encrypted: bytes) -> Dict:
        """Decrypt MCP message."""
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted)