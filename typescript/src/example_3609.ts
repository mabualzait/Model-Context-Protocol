# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.7 Platform-Specific Implementation Details

// pages/api/mcp/[...path].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { MCPClient } from '@modelcontextprotocol/sdk';

// Singleton MCP client for Next.js server
let mcpClient: MCPClient | null = null;

function getMCPClient(): MCPClient {
    if (!mcpClient) {
        mcpClient = new MCPClient({
            transport: 'http',
            url: process.env.MCP_SERVER_URL || 'http://localhost:8080'
        });
        mcpClient.connect();
    }
    return mcpClient;
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    const { path } = req.query;
    const pathArray = Array.isArray(path) ? path : [path];
    
    // Route to MCP method
    const method = pathArray.join('/');
    
    try {
        const client = getMCPClient();
        
        if (req.method === 'GET') {
            // Handle resource/read
            if (method.startsWith('resources/')) {
                const uri = decodeURIComponent(pathArray[pathArray.length - 1] as string);
                const content = await client.readResource(uri);
                return res.status(200).json({ content });
            }
            
            // Handle tools/list, resources/list
            if (method === 'tools/list') {
                const tools = await client.listTools();
                return res.status(200).json({ tools });
            }
            
            if (method === 'resources/list') {
                const resources = await client.listResources();
                return res.status(200).json({ resources });
            }
        }
        
        if (req.method === 'POST') {
            // Handle tools/call
            if (method === 'tools/call') {
                const { name, arguments: arguments_ } = req.body;
                const result = await client.callTool(name, arguments_);
                return res.status(200).json(result);
            }
        }
        
        return res.status(404).json({ error: 'Not found' });
    } catch (error) {
        console.error('MCP API error:', error);
        return res.status(500).json({
            error: 'Internal server error',
            message: error instanceof Error ? error.message : String(error)
        });
    }
}