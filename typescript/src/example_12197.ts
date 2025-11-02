# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.8 Comprehensive Web Application Integration

// pages/api/mcp/tools/[tool].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { MCPClient } from '@modelcontextprotocol/sdk';

let client: MCPClient | null = null;

function getClient(): MCPClient {
    if (!client) {
        client = new MCPClient({
            transport: 'http',
            url: process.env.MCP_SERVER_URL || 'http://localhost:8080'
        });
        client.connect();
    }
    return client;
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    const { tool } = req.query;
    const { arguments: arguments_ } = req.body;
    
    try {
        const mcpClient = getClient();
        const result = await mcpClient.callTool(tool as string, arguments_);
        
        res.status(200).json(result);
    } catch (error) {
        console.error('MCP tool call failed:', error);
        res.status(500).json({
            error: 'Tool call failed',
            message: error instanceof Error ? error.message : String(error)
        });
    }
}

// pages/api/mcp/resources/[resource].ts
export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    const { resource } = req.query;
    const uri = decodeURIComponent(resource as string);
    
    try {
        const mcpClient = getClient();
        const content = await mcpClient.readResource(uri);
        
        res.status(200).json({ content });
    } catch (error) {
        console.error('MCP resource read failed:', error);
        res.status(500).json({
            error: 'Resource read failed',
            message: error instanceof Error ? error.message : String(error)
        });
    }
}