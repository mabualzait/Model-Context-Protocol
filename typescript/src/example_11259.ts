# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.3 Web Application Integration

class WebMCPClient {
    private baseUrl: string;
    private sessionId: string | null = null;
    
    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }
    
    async connect(serverConfigs: any[]): Promise<void> {
        const response = await fetch(`${this.baseUrl}/api/mcp/sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_info: { name: 'web-client', version: '1.0.0' },
                server_configs: serverConfigs
            })
        });
        
        const data = await response.json();
        this.sessionId = data.session_id;
    }
    
    async listResources(): Promise<any[]> {
        const response = await fetch(
            `${this.baseUrl}/api/mcp/sessions/${this.sessionId}/resources`
        );
        const data = await response.json();
        return data.resources || [];
    }
    
    async readResource(uri: string): Promise<string> {
        const encodedUri = encodeURIComponent(uri);
        const response = await fetch(
            `${this.baseUrl}/api/mcp/sessions/${this.sessionId}/resources/${encodedUri}`
        );
        const data = await response.json();
        return data.contents[0]?.text || '';
    }
    
    async callTool(name: string, arguments: any): Promise<any> {
        const response = await fetch(
            `${this.baseUrl}/api/mcp/sessions/${this.sessionId}/tools`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, arguments })
            }
        );
        const data = await response.json();
        return data;
    }
}

// Usage in React component
function MyComponent() {
    const [mcpClient, setMcpClient] = useState<WebMCPClient | null>(null);
    const [resources, setResources] = useState<any[]>([]);
    
    useEffect(() => {
        const client = new WebMCPClient('http://localhost:5000');
        client.connect([
            { transport: 'stdio', command: ['python', '-m', 'filesystem-server'] }
        ]).then(() => {
            setMcpClient(client);
            client.listResources().then(setResources);
        });
    }, []);
    
    const handleReadFile = async (uri: string) => {
        if (mcpClient) {
            const content = await mcpClient.readResource(uri);
            console.log('File content:', content);
        }
    };
    
    return (
        <div>
            {resources.map(resource => (
                <button key={resource.uri} onClick={() => handleReadFile(resource.uri)}>
                    {resource.name}
                </button>
            ))}
        </div>
    );
}