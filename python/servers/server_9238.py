# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.3 Implementing Tools

import requests
from typing import Dict, Any
from mcp import Tool

class WebSearchTools:
    """Web search tool implementation."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.example.com/v1"
    
    def list_tools(self) -> List[Tool]:
        """List available tools."""
        return [
            Tool(
                name="web_search",
                description="Search the web for information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            )
        ]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        if name == "web_search":
            return self._web_search(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def _web_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Web search tool."""
        query = args["query"]
        max_results = args.get("max_results", 10)
        
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={
                    "q": query,
                    "max_results": max_results,
                    "api_key": self.api_key
                },
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            
            # Format results
            formatted_results = []
            for result in results.get("results", [])[:max_results]:
                formatted_results.append(
                    f"Title: {result.get('title', 'N/A')}\n"
                    f"URL: {result.get('url', 'N/A')}\n"
                    f"Snippet: {result.get('snippet', 'N/A')}\n"
                )
            
            result_text = "\n---\n".join(formatted_results)
            
            return {
                "content": [{"type": "text", "text": result_text}],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True
            }