# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.7 Platform-Specific Implementation Details

// Mobile MCP Client with optimization
import { MCPClient } from '@modelcontextprotocol/sdk/browser';

class MobileMCPClient extends MCPClient {
    private cache: Map<string, CacheEntry>;
    private networkMonitor: NetworkMonitor;
    
    constructor(config: ClientConfig) {
        // Mobile-optimized config
        super({
            ...config,
            timeout: 10000,  // 10s timeout for mobile
            retryConfig: {
                maxRetries: 2,
                retryDelay: 1000
            }
        });
        
        this.cache = new Map();
        this.networkMonitor = new NetworkMonitor();
        
        // Monitor network changes
        this.networkMonitor.on('online', () => {
            this.reconnect();
        });
        
        this.networkMonitor.on('offline', () => {
            // Use cached data when offline
            this.enableCacheOnlyMode();
        });
    }
    
    async readResource(uri: string, useCache: boolean = true): Promise<string> {
        // Check cache first
        if (useCache && this.cache.has(uri)) {
            const entry = this.cache.get(uri)!;
            if (!entry.isExpired()) {
                return entry.data;
            }
        }
        
        // Check network before request
        if (!this.networkMonitor.isOnline()) {
            throw new Error('Network offline');
        }
        
        // Fetch and cache
        const content = await super.readResource(uri);
        
        if (useCache) {
            this.cache.set(uri, new CacheEntry(content, 300));  // 5min TTL
        }
        
        return content;
    }
    
    async callTool(name: string, arguments_: Record<string, any>): Promise<any> {
        // Mobile: Show loading indicator
        this.showLoadingIndicator();
        
        try {
            const result = await super.callTool(name, arguments_);
            return result;
        } finally {
            this.hideLoadingIndicator();
        }
    }
    
    private showLoadingIndicator() {
        // Show native loading indicator
        // Implementation depends on React Native library
    }
    
    private hideLoadingIndicator() {
        // Hide native loading indicator
    }
}