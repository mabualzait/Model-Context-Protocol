# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.4 Tool Invocation Patterns

class MCPClient:
    def call_tool(self, name, arguments):
        """Call a tool with arguments"""
        # Validate tool exists
        if name not in self.session.tools:
            raise ValueError(f"Tool not found: {name}")
        
        tool = self.session.tools[name]
        
        # Validate arguments against schema
        self._validate_arguments(arguments, tool.get("inputSchema", {}))
        
        request = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        response = self._send_request(request)
        
        if response.get("error"):
            raise ValueError(f"Tool call failed: {response['error']}")
        
        result = response["result"]
        
        # Check for errors
        if result.get("isError"):
            raise RuntimeError(f"Tool execution error: {result.get('content', [{}])[0].get('text', 'Unknown error')}")
        
        # Process content
        content = result.get("content", [])
        return self._process_tool_content(content)
    
    def _validate_arguments(self, arguments, schema):
        """Validate arguments against schema"""
        if not schema:
            return
        
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        for key in required:
            if key not in arguments:
                raise ValueError(f"Required argument missing: {key}")
        
        for key, value in arguments.items():
            if key in properties:
                prop_schema = properties[key]
                expected_type = prop_schema.get("type")
                
                if expected_type == "string" and not isinstance(value, str):
                    raise ValueError(f"Argument {key} must be string")
                elif expected_type == "integer" and not isinstance(value, int):
                    raise ValueError(f"Argument {key} must be integer")
                elif expected_type == "object" and not isinstance(value, dict):
                    raise ValueError(f"Argument {key} must be object")
    
    def _process_tool_content(self, content):
        """Process tool content"""
        results = []
        for item in content:
            if item.get("type") == "text":
                results.append(item.get("text"))
            elif item.get("type") == "image":
                results.append(item.get("data"))
            elif item.get("type") == "resource"):
                results.append(item.get("uri"))
        
        return results