# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.2 Legacy System Integration

class MockSOAPClient:
    """Mock SOAP client for testing."""
    
    def __init__(self, wsdl_url: str):
        self.wsdl_url = wsdl_url
        self.methods: Dict[str, callable] = {}
    
    def call(self, method_name: str, params: Dict) -> Any:
        """Call SOAP method."""
        if method_name in self.methods:
            return self.methods[method_name](params)
        else:
            return {"result": "mock_response", "params": params}