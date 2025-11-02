# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.5 Detailed Platform Implementation Examples

// Claude Desktop MCP Host (simplified)
import { MCPServer, MCPClient } from '@modelcontextprotocol/sdk';

class ClaudeDesktopHost {
    private servers: Map<string, MCPServer> = new Map();
    private sessions: Map<string, MCPSession> = new Map();
    
    constructor() {
        this.loadServerConfigs();
        this.initializeServers();
    }
    
    private loadServerConfigs() {
        // Load from Claude Desktop config
        const config = this.loadConfig();
        const serverConfigs = config.mcpServers || {};
        
        for (const [serverId, config] of Object.entries(serverConfigs)) {
            this.registerServer(serverId, config);
        }
    }
    
    private registerServer(serverId: string, config: ServerConfig) {
        const server = new MCPServer({
            transport: config.transport || 'stdio',
            command: config.command,
            args: config.args || [],
            env: config.env || {}
        });
        
        this.servers.set(serverId, server);
    }
    
    async initializeServers() {
        for (const [serverId, server] of this.servers) {
            try {
                await server.connect();
                await server.initialize({
                    protocolVersion: "2024-11-05",
                    capabilities: {},
                    clientInfo: {
                        name: "claude-desktop",
                        version: "1.0.0"
                    }
                });
                
                console.log(`MCP server ${serverId} initialized`);
            } catch (error) {
                console.error(`Failed to initialize server ${serverId}:`, error);
            }
        }
    }
    
    async getAvailableTools(): Promise<Tool[]> {
        const allTools: Tool[] = [];
        
        for (const [serverId, server] of this.servers) {
            try {
                const tools = await server.listTools();
                allTools.push(...tools.map(tool => ({
                    ...tool,
                    serverId
                })));
            } catch (error) {
                console.error(`Failed to list tools from ${serverId}:`, error);
            }
        }
        
        return allTools;
    }
    
    async invokeTool(serverId: string, toolName: string, arguments: any) {
        const server = this.servers.get(serverId);
        if (!server) {
            throw new Error(`Server not found: ${serverId}`);
        }
        
        return await server.callTool(toolName, arguments);
    }
}