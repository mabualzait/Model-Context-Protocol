# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.8 Comprehensive Web Application Integration

import React, { useEffect, useState } from 'react';
import { MCPClient } from '@modelcontextprotocol/sdk';

interface MCPProviderProps {
    children: React.ReactNode;
}

const MCPContext = React.createContext<MCPClient | null>(null);

export function MCPProvider({ children }: MCPProviderProps) {
    const [client, setClient] = useState<MCPClient | null>(null);
    
    useEffect(() => {
        const mcpClient = new MCPClient({
            transport: 'sse',
            url: 'http://localhost:8080/sse'
        });
        
        mcpClient.connect().then(() => {
            setClient(mcpClient);
        }).catch(error => {
            console.error('MCP connection failed:', error);
        });
        
        return () => {
            mcpClient.disconnect();
        };
    }, []);
    
    return (
        <MCPContext.Provider value={client}>
            {children}
        </MCPContext.Provider>
    );
}

export function useMCP() {
    const client = React.useContext(MCPContext);
    
    if (!client) {
        throw new Error('useMCP must be used within MCPProvider');
    }
    
    return client;
}

// Custom hook for MCP resources
export function useMCPResource(uri: string) {
    const client = useMCP();
    const [content, setContent] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    
    useEffect(() => {
        client.readResource(uri)
            .then(setContent)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [client, uri]);
    
    return { content, loading, error };
}

// Custom hook for MCP tools
export function useMCPTool(toolName: string) {
    const client = useMCP();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    
    const invoke = async (arguments_: Record<string, any>) => {
        setLoading(true);
        setError(null);
        
        try {
            const result = await client.callTool(toolName, arguments_);
            return result;
        } catch (e) {
            const err = e instanceof Error ? e : new Error(String(e));
            setError(err);
            throw err;
        } finally {
            setLoading(false);
        }
    };
    
    return { invoke, loading, error };
}

// Example component using MCP
function DocumentViewer({ uri }: { uri: string }) {
    const { content, loading, error } = useMCPResource(uri);
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    
    return <div>{content}</div>;
}

function ToolPanel() {
    const client = useMCP();
    const [tools, setTools] = useState<any[]>([]);
    
    useEffect(() => {
        client.listTools().then(setTools);
    }, [client]);
    
    return (
        <div>
            <h2>Available Tools</h2>
            {tools.map(tool => (
                <ToolButton key={tool.name} tool={tool} />
            ))}
        </div>
    );
}

function ToolButton({ tool }: { tool: any }) {
    const { invoke, loading } = useMCPTool(tool.name);
    
    const handleClick = async () => {
        try {
            const result = await invoke({ /* arguments */ });
            console.log('Tool result:', result);
        } catch (error) {
            console.error('Tool invocation failed:', error);
        }
    };
    
    return (
        <button onClick={handleClick} disabled={loading}>
            {tool.name}
        </button>
    );
}