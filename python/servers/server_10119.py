# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.5 Troubleshooting Common Issues

class ConnectionDiagnostics:
    """Diagnose connection issues."""
    
    def diagnose_connection(self, endpoint: str, transport: str):
        """Diagnose connection problems."""
        print(f"Testing connection to {endpoint} via {transport}")
        
        # Test basic connectivity
        if transport == "http":
            import requests
            try:
                response = requests.get(endpoint, timeout=5)
                print(f"✓ HTTP endpoint reachable: {response.status_code}")
            except requests.RequestException as e:
                print(f"✗ HTTP endpoint unreachable: {e}")
        
        # Test MCP protocol
        try:
            client = MCPClient(endpoint, transport=transport)
            client.connect()
            print("✓ MCP connection established")
            
            # Test initialize
            init_result = client._initialize()
            print(f"✓ Initialize successful: {init_result}")
            
        except Exception as e:
            print(f"✗ MCP connection failed: {e}")
            import traceback
            traceback.print_exc()