# 📖 Chapter: Chapter 1: Introduction to Model Context Protocol
# 📖 Section: 1.9 Detailed Use Cases and Implementation Examples

# Multi-Server Client for Workflow Orchestration
class WorkflowOrchestrator:
    """Orchestrates workflows using multiple MCP servers."""
    
    def __init__(self):
        self.clients = {
            "filesystem": MCPClient("stdio", "fs-server"),
            "database": MCPClient("http", "https://db-server.example.com"),
            "api": MCPClient("http", "https://api-server.example.com")
        }
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all MCP clients."""
        for name, client in self.clients.items():
            client.connect()
    
    async def analyze_codebase(self, project_path: str):
        """Analyze codebase using multiple tools."""
        # Step 1: Read project files
        files_client = self.clients["filesystem"]
        files = files_client.list_resources()
        
        # Step 2: Analyze each file
        analysis_results = []
        for file_resource in files:
            if file_resource["uri"].startswith(f"file://{project_path}"):
                content = files_client.read_resource(file_resource["uri"])
                
                # Use AI tool to analyze
                analysis = await self._analyze_code(content)
                analysis_results.append({
                    "file": file_resource["uri"],
                    "analysis": analysis
                })
        
        # Step 3: Store results in database
        db_client = self.clients["database"]
        db_client.call_tool("insert", {
            "table": "code_analysis",
            "data": {
                "project_path": project_path,
                "results": json.dumps(analysis_results),
                "timestamp": datetime.now().isoformat()
            }
        })
        
        return analysis_results
    
    async def _analyze_code(self, content: str) -> Dict:
        """Analyze code content."""
        # This would use an AI model to analyze the code
        # Implementation depends on AI provider
        pass