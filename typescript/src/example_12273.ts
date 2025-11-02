# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.9 Mobile Application Integration

import React, { useEffect, useState } from 'react';
import { View, Text, Button, TextInput } from 'react-native';
import { MCPClient } from '@modelcontextprotocol/sdk/browser';

export function MCPMobileApp() {
    const [client, setClient] = useState<MCPClient | null>(null);
    const [tools, setTools] = useState<any[]>([]);
    const [resources, setResources] = useState<any[]>([]);
    
    useEffect(() => {
        const mcpClient = new MCPClient({
            transport: 'http',
            url: 'https://mcp-server.example.com',
            timeout: 10000 // 10 second timeout for mobile
        });
        
        mcpClient.connect()
            .then(() => {
                setClient(mcpClient);
                return Promise.all([
                    mcpClient.listTools(),
                    mcpClient.listResources()
                ]);
            })
            .then(([toolsList, resourcesList]) => {
                setTools(toolsList);
                setResources(resourcesList);
            })
            .catch(error => {
                console.error('MCP connection failed:', error);
            });
    }, []);
    
    const handleToolCall = async (toolName: string) => {
        if (!client) return;
        
        try {
            const result = await client.callTool(toolName, {});
            console.log('Tool result:', result);
        } catch (error) {
            console.error('Tool call failed:', error);
        }
    };
    
    return (
        <View>
            <Text>MCP Tools</Text>
            {tools.map(tool => (
                <Button
                    key={tool.name}
                    title={tool.name}
                    onPress={() => handleToolCall(tool.name)}
                />
            ))}
            
            <Text>MCP Resources</Text>
            {resources.map(resource => (
                <Text key={resource.uri}>{resource.name}</Text>
            ))}
        </View>
    );
}