# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.2 Legacy System Integration

class ProtocolTranslator:
    """Translate between different protocols and MCP."""
    
    def __init__(self):
        self.translators: Dict[str, callable] = {}
    
    def register_translator(self, source_protocol: str, 
                           translator: callable):
        """Register protocol translator."""
        self.translators[source_protocol] = translator
    
    def translate_to_mcp(self, source_protocol: str, 
                         data: Any) -> Dict:
        """Translate data from source protocol to MCP format."""
        if source_protocol not in self.translators:
            raise ValueError(f"No translator for protocol: {source_protocol}")
        
        translator = self.translators[source_protocol]
        return translator(data)
    
    def translate_from_mcp(self, target_protocol: str,
                          mcp_data: Dict) -> Any:
        """Translate data from MCP format to target protocol."""
        if target_protocol not in self.translators:
            raise ValueError(f"No translator for protocol: {target_protocol}")
        
        translator = self.translators[target_protocol]
        return translator(mcp_data)