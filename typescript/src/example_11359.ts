# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.4 Mobile Application Considerations

// React Native example
import { MCPClient } from '@modelcontextprotocol/client';

class MobileMCPClient {
    private baseUrl: string;
    private sessionId: string | null = null;
    private isOnline: boolean = true;
    
    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
        this.setupNetworkListener();
    }
    
    setupNetworkListener() {
        // Monitor network connectivity
        NetInfo.addEventListener(state => {
            this.isOnline = state.isConnected;
        });
    }
    
    async connect(serverConfigs: any[]): Promise<void> {
        if (!this.isOnline) {
            throw new Error('No network connection');
        }
        
        // Use HTTP/SSE transport for mobile
        const httpConfig = serverConfigs.map(config => ({
            ...config,
            transport: 'http',
            url: `${this.baseUrl}/mcp/${config.name}`
        }));
        
        const response = await fetch(`${this.baseUrl}/api/mcp/sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_info: { name: 'mobile-client', version: '1.0.0' },
                server_configs: httpConfig
            })
        });
        
        const data = await response.json();
        this.sessionId = data.session_id;
    }
    
    async callToolWithRetry(name: string, arguments: any, maxRetries = 3): Promise<any> {
        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                return await this.callTool(name, arguments);
            } catch (error) {
                if (attempt === maxRetries - 1) throw error;
                await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
            }
        }
    }
}