# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.5 Detailed Platform Implementation Examples

# Replit MCP Integration
from replit import db
import subprocess
from mcp_client import MCPClient

class ReplitMCPIntegration:
    """MCP integration for Replit workspace."""
    
    def __init__(self):
        self.workspace_root = "/home/runner"
        self.client = MCPClient("stdio", "replit-mcp-server")
        self.client.connect()
    
    def expose_workspace_files(self):
        """Expose Replit workspace files via MCP."""
        # Replit exposes files through MCP server
        # Files are accessible via file:// URIs
        files = self.client.list_resources()
        
        for file_resource in files:
            if file_resource["uri"].startswith("file://"):
                # File is accessible via MCP
                print(f"Available: {file_resource['name']}")
    
    def use_ai_with_context(self, ai_prompt: str):
        """Use AI with full workspace context."""
        # Get relevant files for context
        relevant_files = self.find_relevant_files(ai_prompt)
        
        # Read files via MCP
        context = []
        for file_path in relevant_files:
            content = self.client.read_resource(f"file://{file_path}")
            context.append(f"File: {file_path}\n{content}")
        
        # Use AI with context
        full_context = "\n\n".join(context)
        enhanced_prompt = f"{ai_prompt}\n\nContext:\n{full_context}"
        
        return enhanced_prompt
    
    def find_relevant_files(self, prompt: str) -> List[str]:
        """Find files relevant to prompt."""
        # Use MCP tools to search files
        result = self.client.call_tool("search_files", {
            "query": prompt,
            "root": self.workspace_root
        })
        
        return result.get("files", [])