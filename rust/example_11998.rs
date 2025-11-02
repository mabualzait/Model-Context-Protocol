# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.7 Detailed IDE Integration Examples

use mcp::Client;
use zed::LanguageServerId;

pub struct MCPLanguageServer {
    client: Client,
    server_id: LanguageServerId,
}

impl MCPLanguageServer {
    pub fn new(server_id: LanguageServerId) -> Result<Self, Error> {
        let client = Client::new_stdio("mcp-server")?;
        client.connect()?;
        
        Ok(Self {
            client,
            server_id,
        })
    }
    
    pub fn initialize(&mut self) -> Result<(), Error> {
        // Initialize MCP connection
        let init_result = self.client.initialize(InitParams {
            protocol_version: "2024-11-05".to_string(),
            capabilities: Default::default(),
            client_info: ClientInfo {
                name: "zed-editor".to_string(),
                version: "1.0.0".to_string(),
            },
        })?;
        
        // Discover capabilities
        let tools = self.client.list_tools()?;
        let resources = self.client.list_resources()?;
        
        // Register with Zed
        self.register_tools(tools);
        self.register_resources(resources);
        
        Ok(())
    }
    
    pub fn get_resource_content(&self, uri: &str) -> Result<String, Error> {
        self.client.read_resource(uri)
    }
    
    pub fn invoke_tool(&self, name: &str, arguments: serde_json::Value) -> Result<serde_json::Value, Error> {
        self.client.call_tool(name, arguments)
    }
}