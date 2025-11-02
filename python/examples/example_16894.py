# 📖 Chapter: Chapter 13: Multi-Agent Systems with MCP
# 📖 Section: 13.5 Case Studies: Complex Multi-Agent Systems

class DocumentProcessingMultiAgentSystem:
    """Multi-agent system for document processing."""
    
    def __init__(self, orchestrator: MultiAgentOrchestrator):
        self.orchestrator = orchestrator
        self.communication = AgentCommunicationManager(orchestrator)
        self.shared_state = SharedStateManager(orchestrator)
    
    def process_document(self, document_id: str, document_path: str) -> Dict:
        """Process document through multi-agent pipeline."""
        # Define workflow
        workflow = {
            "workflow_id": f"doc_process_{document_id}",
            "tasks": [
                {
                    "id": "extract",
                    "type": "extraction",
                    "required_capabilities": ["text_extraction"],
                    "input": {"document_path": document_path}
                },
                {
                    "id": "analyze",
                    "type": "analysis",
                    "required_capabilities": ["content_analysis"],
                    "input": {"document_id": document_id}
                },
                {
                    "id": "summarize",
                    "type": "summarization",
                    "required_capabilities": ["summarization"],
                    "input": {"document_id": document_id}
                },
                {
                    "id": "validate",
                    "type": "validation",
                    "required_capabilities": ["validation"],
                    "input": {"document_id": document_id}
                },
                {
                    "id": "store",
                    "type": "storage",
                    "required_capabilities": ["data_storage"],
                    "input": {"document_id": document_id}
                }
            ]
        }
        
        # Execute workflow
        result = self.orchestrator.coordinate_workflow(
            workflow["workflow_id"],
            workflow["tasks"]
        )
        
        return result