# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.7 Platform-Specific Implementation Details

// Claude Desktop MCP Host
class ClaudeDesktopMCPHost {
    private host: MCPHost;
    private serverRegistry: Map<string, ServerConfig>;
    
    constructor() {
        this.host = new MCPHost();
        this.serverRegistry = new Map();
        this.loadConfiguration();
    }
    
    private loadConfiguration() {
        // Load from Claude Desktop config file
        const configPath = this.getConfigPath();
        const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
        
        for (const [serverId, serverConfig] of Object.entries(config.mcpServers)) {
            this.registerServer(serverId, serverConfig);
        }
    }
    
    private registerServer(serverId: string, config: ServerConfig) {
        // Register server with host
        this.host.registerServer(serverId, {
            transport: config.transport || 'stdio',
            command: config.command,
            args: config.args || [],
            env: config.env || {}
        });
        
        this.serverRegistry.set(serverId, config);
    }
    
    async initialize() {
        // Initialize all servers
        await this.host.initializeAllServers();
        
        // Discover capabilities
        const capabilities = await this.host.discoverCapabilities();
        
        // Expose to Claude AI
        this.exposeToClaude(capabilities);
    }
    
    private exposeToClaude(capabilities: Map<string, ServerCapabilities>) {
        // Make capabilities available to Claude AI
        // This allows Claude to use MCP servers transparently
        for (const [serverId, caps] of capabilities) {
            console.log(`Server ${serverId}: ${caps.tools.length} tools, ${caps.resources.length} resources`);
        }
    }
}