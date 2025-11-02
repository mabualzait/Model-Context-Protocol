# 📖 Chapter: Chapter 9: Advanced MCP Patterns
# 📖 Section: 9.1 Multi-Server Architectures

from typing import Dict, List, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

class MultiServerMCPClient:
    """Client that aggregates multiple MCP servers."""
    
    def __init__(self, server_configs: List[Dict]):
        self.servers: Dict[str, 'MCPClient'] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Initialize connections to all servers
        for config in server_configs:
            server_id = config['id']
            endpoint = config['endpoint']
            transport = config.get('transport', 'stdio')
            
            client = MCPClient(endpoint, transport=transport)
            client.connect()
            self.servers[server_id] = client
    
    def list_all_resources(self) -> Dict[str, List[Dict]]:
        """List resources from all servers."""
        all_resources = {}
        
        for server_id, client in self.servers.items():
            try:
                resources = client.list_resources()
                all_resources[server_id] = resources
            except Exception as e:
                print(f"Error listing resources from {server_id}: {e}")
        
        return all_resources
    
    def list_all_tools(self) -> Dict[str, List[Dict]]:
        """List tools from all servers."""
        all_tools = {}
        
        for server_id, client in self.servers.items():
            try:
                tools = client.list_tools()
                all_tools[server_id] = tools
            except Exception as e:
                print(f"Error listing tools from {server_id}: {e}")
        
        return all_tools
    
    def find_resource(self, uri: str) -> Optional[Dict]:
        """Find resource across all servers."""
        for server_id, client in self.servers.items():
            try:
                resources = client.list_resources()
                matching = [r for r in resources if r.get('uri') == uri]
                if matching:
                    return {
                        'server_id': server_id,
                        'resource': matching[0]
                    }
            except Exception:
                continue
        
        return None
    
    def find_tool(self, tool_name: str) -> Optional[Dict]:
        """Find tool across all servers."""
        for server_id, client in self.servers.items():
            try:
                tools = client.list_tools()
                matching = [t for t in tools if t.get('name') == tool_name]
                if matching:
                    return {
                        'server_id': server_id,
                        'tool': matching[0]
                    }
            except Exception:
                continue
        
        return None
    
    async def call_tool_async(self, server_id: str, tool_name: str, 
                             arguments: Dict) -> Dict:
        """Call tool asynchronously."""
        if server_id not in self.servers:
            raise ValueError(f"Server {server_id} not found")
        
        client = self.servers[server_id]
        
        # Run in thread pool for async compatibility
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            client.call_tool,
            tool_name,
            arguments
        )
        
        return result
    
    def aggregate_search(self, query: str, servers: List[str] = None) -> List[Dict]:
        """Search across multiple servers and aggregate results."""
        if servers is None:
            servers = list(self.servers.keys())
        
        all_results = []
        
        for server_id in servers:
            if server_id not in self.servers:
                continue
            
            # Check if server has search tool
            tool_info = self.find_tool('search')
            if tool_info and tool_info['server_id'] == server_id:
                try:
                    client = self.servers[server_id]
                    result = client.call_tool('search', {'query': query})
                    all_results.append({
                        'server_id': server_id,
                        'results': result
                    })
                except Exception as e:
                    print(f"Error searching {server_id}: {e}")
        
        return all_results