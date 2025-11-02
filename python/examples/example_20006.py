# 📖 Chapter: Appendices
# 📖 Section: A.3 Complete Application Examples

#!/usr/bin/env python3
"""
Complete MCP Application - Document Analysis System
This application uses MCP to analyze documents through multiple specialized servers.
"""

from mcp_client import MCPClient
from typing import List, Dict
import json

class DocumentAnalysisApp:
    """Document analysis application using MCP."""
    
    def __init__(self):
        self.file_server = MCPClient("http://localhost:8081", "http")
        self.analysis_server = MCPClient("http://localhost:8082", "http")
        self.summary_server = MCPClient("http://localhost:8083", "http")
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize connections to MCP servers."""
        self.file_server.connect()
        self.analysis_server.connect()
        self.summary_server.connect()
    
    def analyze_document(self, document_path: str) -> Dict:
        """Analyze document using multiple MCP servers."""
        # Step 1: Read document
        content = self.file_server.call_tool("read_file", {"path": document_path})
        
        if content.get("isError"):
            return {"error": "Failed to read document"}
        
        document_text = content["content"][0]["text"]
        
        # Step 2: Analyze content
        analysis = self.analysis_server.call_tool(
            "analyze_text",
            {"text": document_text}
        )
        
        # Step 3: Generate summary
        summary = self.summary_server.call_tool(
            "summarize",
            {"text": document_text}
        )
        
        return {
            "document_path": document_path,
            "analysis": analysis.get("content", [{}])[0].get("text", ""),
            "summary": summary.get("content", [{}])[0].get("text", "")
        }
    
    def batch_analyze(self, document_paths: List[str]) -> List[Dict]:
        """Analyze multiple documents."""
        results = []
        
        for path in document_paths:
            try:
                result = self.analyze_document(path)
                results.append(result)
            except Exception as e:
                results.append({
                    "document_path": path,
                    "error": str(e)
                })
        
        return results

if __name__ == "__main__":
    app = DocumentAnalysisApp()
    
    result = app.analyze_document("/path/to/document.txt")
    print(json.dumps(result, indent=2))