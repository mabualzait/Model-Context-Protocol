# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.7 Detailed IDE Integration Examples

import * as vscode from 'vscode';
import { MCPClient } from '@modelcontextprotocol/sdk';

class MCPExtension {
    private client: MCPClient;
    private outputChannel: vscode.OutputChannel;
    
    constructor(context: vscode.ExtensionContext) {
        this.outputChannel = vscode.window.createOutputChannel('MCP');
        this.client = new MCPClient({
            transport: 'stdio',
            command: 'mcp-server',
            args: []
        });
        
        this.initialize();
    }
    
    private async initialize() {
        try {
            await this.client.connect();
            
            // Discover available tools
            const tools = await this.client.listTools();
            
            // Register commands for each tool
            for (const tool of tools) {
                vscode.commands.registerCommand(
                    `mcp.${tool.name}`,
                    async () => await this.invokeTool(tool.name)
                );
            }
            
            // Discover resources
            const resources = await this.client.listResources();
            
            // Register resource providers
            for (const resource of resources) {
                this.registerResourceProvider(resource);
            }
            
            vscode.window.showInformationMessage('MCP extension initialized');
        } catch (error) {
            vscode.window.showErrorMessage(`MCP initialization failed: ${error}`);
        }
    }
    
    private async invokeTool(toolName: string) {
        try {
            // Show input dialog for tool arguments
            const input = await vscode.window.showInputBox({
                prompt: `Enter arguments for ${toolName}`,
                placeHolder: 'JSON arguments'
            });
            
            if (!input) {
                return;
            }
            
            const arguments_ = JSON.parse(input);
            const result = await this.client.callTool(toolName, arguments_);
            
            // Display result
            this.outputChannel.appendLine(`Tool ${toolName} result:`);
            this.outputChannel.appendLine(JSON.stringify(result, null, 2));
            this.outputChannel.show();
        } catch (error) {
            vscode.window.showErrorMessage(`Tool invocation failed: ${error}`);
        }
    }
    
    private registerResourceProvider(resource: Resource) {
        // Create resource provider for VS Code
        const provider = new class implements vscode.TextDocumentContentProvider {
            provideTextDocumentContent(uri: vscode.Uri): Thenable<string> {
                return this.client.readResource(resource.uri);
            }
        };
        
        vscode.workspace.registerTextDocumentContentProvider(
            `mcp-${resource.name}`,
            provider
        );
    }
    
    dispose() {
        this.client.disconnect();
    }
}

export function activate(context: vscode.ExtensionContext) {
    const extension = new MCPExtension(context);
    context.subscriptions.push(extension);
}