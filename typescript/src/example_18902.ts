# 📖 Chapter: Chapter 15: The Future of MCP
# 📖 Section: 15.3 Community and Ecosystem Growth

// Official TypeScript MCP SDK example
import { MCPServer, MCPClient } from '@modelcontextprotocol/sdk';

// Server implementation
const server = new MCPServer('my-server');

server.resource('file://*', (uri: string) => {
  return {
    uri,
    name: uri.split('/').pop() || uri,
    description: `File: ${uri}`
  };
});

server.tool('read_file', async (params: { path: string }) => {
  const fs = await import('fs/promises');
  return await fs.readFile(params.path, 'utf-8');
});

// Client implementation
const client = new MCPClient('http://localhost:8080');
await client.connect();

const resources = await client.listResources();
const content = await client.readResource('file://example.txt');
const result = await client.callTool('read_file', { path: 'example.txt' });