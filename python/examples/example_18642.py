# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.2 Protocol Evolution and Roadmap

class ProtocolVersionManager:
    """Manage MCP protocol version compatibility."""
    
    def __init__(self):
        self.supported_versions = [
            "2024-11-05",  # Initial release
            "2024-12-01",  # Streaming support
            "2025-01-01"   # Future: Enhanced security
        ]
        self.compatibility_matrix = {
            "2024-11-05": {
                "compatible_with": ["2024-12-01"],
                "migration_required": ["2025-01-01"]
            },
            "2024-12-01": {
                "compatible_with": ["2024-11-05"],
                "migration_required": ["2025-01-01"]
            }
        }
    
    def check_compatibility(self, client_version: str, 
                           server_version: str) -> Dict:
        """Check version compatibility."""
        client_compat = self.compatibility_matrix.get(client_version, {})
        compatible = server_version in client_compat.get("compatible_with", [])
        
        return {
            "compatible": compatible,
            "client_version": client_version,
            "server_version": server_version,
            "migration_needed": server_version in client_compat.get(
                "migration_required", []
            ),
            "recommendations": self._get_recommendations(
                client_version, server_version
            )
        }
    
    def _get_recommendations(self, client_version: str, 
                            server_version: str) -> List[str]:
        """Get migration recommendations."""
        recommendations = []
        
        # Check if upgrade needed
        if client_version < server_version:
            recommendations.append(f"Consider upgrading client to {server_version}")
        
        # Check for breaking changes
        if self._has_breaking_changes(client_version, server_version):
            recommendations.append("Review migration guide for breaking changes")
            recommendations.append("Update implementation before upgrading")
        
        return recommendations
    
    def _has_breaking_changes(self, from_version: str, 
                             to_version: str) -> bool:
        """Check if migration involves breaking changes."""
        # Simplified check (in practice, detailed analysis)
        major_from = from_version.split('-')[0]
        major_to = to_version.split('-')[0]
        
        return major_from != major_to