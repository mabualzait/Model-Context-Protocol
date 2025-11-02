# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.2 Protocol Evolution and Roadmap

class BatchMCPExtension:
    """Extension for batch operations."""
    
    def batch_operations(self, operations: List[Dict]) -> List[Dict]:
        """Execute multiple operations in batch."""
        results = []
        
        for operation in operations:
            try:
                method = operation.get("method")
                params = operation.get("params", {})
                result = self.execute_method(method, params)
                results.append({
                    "id": operation.get("id"),
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                results.append({
                    "id": operation.get("id"),
                    "status": "error",
                    "error": str(e)
                })
        
        return results