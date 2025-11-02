# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.6 Advanced Integration Patterns

class DataPipelineMCPServer:
    """MCP server for data pipeline operations."""
    
    def __init__(self):
        self.pipelines: Dict[str, 'DataPipeline'] = {}
        self.server = MCPServer(
            name="data-pipeline-server",
            version="1.0.0"
        )
        self._register_handlers()
    
    def register_pipeline(self, pipeline_id: str, pipeline: 'DataPipeline'):
        """Register a data pipeline."""
        self.pipelines[pipeline_id] = pipeline
        
        # Expose pipeline stages as MCP resources
        for stage in pipeline.stages:
            resource_uri = f"pipeline://{pipeline_id}/{stage.name}"
            self.server.register_resource({
                "uri": resource_uri,
                "name": stage.name,
                "description": stage.description,
                "mimeType": "application/json"
            })
    
    def register_tools(self):
        """Register pipeline tools."""
        self.server.register_tool({
            "name": "run_pipeline",
            "description": "Execute a data pipeline",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "pipeline_id": {"type": "string"},
                    "input_data": {"type": "string"}
                },
                "required": ["pipeline_id", "input_data"]
            }
        })
    
    def _handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        """Handle pipeline tool call."""
        if name == "run_pipeline":
            pipeline_id = arguments["pipeline_id"]
            input_data = json.loads(arguments["input_data"])
            
            if pipeline_id not in self.pipelines:
                raise ValueError(f"Pipeline not found: {pipeline_id}")
            
            pipeline = self.pipelines[pipeline_id]
            result = pipeline.execute(input_data)
            
            return {
                "content": [{"type": "text", "text": json.dumps(result)}]
            }
        
        raise ValueError(f"Unknown tool: {name}")