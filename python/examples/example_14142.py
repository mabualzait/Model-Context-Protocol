# 📖 Chapter: Chapter 10: Security Considerations in MCP
# 📖 Section: 10.5 Network Security and TLS

import ssl
import socket
from typing import Optional

class SecureMCPServer:
    """MCP server with TLS support."""
    
    def __init__(self, cert_file: str, key_file: str):
        self.cert_file = cert_file
        self.key_file = key_file
        self.ssl_context = self._create_ssl_context()
    
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Create secure SSL context."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        
        # Load certificate and key
        context.load_cert_chain(self.cert_file, self.key_file)
        
        # Disable weak protocols
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Strong cipher suites
        context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!SRP:!CAMELLIA')
        
        # Certificate verification
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        
        return context
    
    def create_secure_connection(self, host: str, port: int):
        """Create secure TLS connection."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = self.ssl_context.wrap_socket(sock, server_hostname=host)
        secure_sock.connect((host, port))
        return secure_sock