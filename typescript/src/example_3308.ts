# 📖 Chapter: Chapter 3: MCP in the Ecosystem
# 📖 Section: 3.5 Detailed Platform Implementation Examples

// VS Code MCP Extension
import * as vscode from 'vscode';
import { MCPClient } from '@modelcontextprotocol/sdk';

class VSCodeMCPExtension {
    private client: MCPClient;
    private context: vscode.ExtensionContext;
    
    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.initializeMCP();
    }
    
    private async initializeMCP() {
        // Get MCP server config from VS Code settings
        const config = vscode.workspace.getConfiguration('mcp');
        const serverCommand = config.get<string>('serverCommand');
        
        if (!serverCommand) {
            vscode.window.showWarningMessage('MCP server command not configured');
            return;
        }
        
        this.client = new MCPClient({
            transport: 'stdio',
            command: serverCommand,
            args: []
        });
        
        try {
            await this.client.connect();
            
            // Register commands for MCP tools
            const tools = await this.client.listTools();
            for (const tool of tools) {
                const commandId = `mcp.${tool.name}`;
                vscode.commands.registerCommand(commandId, async () => {
                    await this.invokeTool(tool);
                });
            }
            
            // Register resource providers
            const resources = await this.client.listResources();
            for (const resource of resources) {
                this.registerResourceProvider(resource);
            }
            
            vscode.window.showInformationMessage(`MCP extension initialized with ${tools.length} tools`);
        } catch (error) {
            vscode.window.showErrorMessage(`MCP initialization failed: ${error}`);
        }
    }
    
    private async invokeTool(tool: Tool) {
        // Show input dialog for tool arguments
        const input = await vscode.window.showInputBox({
            prompt: `Enter arguments for ${tool.name}`,
            placeHolder: 'JSON format',
            validateInput: (value) => {
                try {
                    JSON.parse(value);
                    return null;
                } catch {
                    return 'Invalid JSON';
                }
            }
        });
        
        if (!input) {
            return;
        }
        
        try {
            const arguments_ = JSON.parse(input);
            const result = await this.client.callTool(tool.name, arguments_);
            
            // Display result in output panel
            const outputChannel = vscode.window.createOutputChannel(`MCP: ${tool.name}`);
            outputChannel.appendLine(`Tool: ${tool.name}`);
            outputChannel.appendLine(`Result:`);
            outputChannel.appendLine(JSON.stringify(result, null, 2));
            outputChannel.show();
        } catch (error) {
            vscode.window.showErrorMessage(`Tool invocation failed: ${error}`);
        }
    }
    
    private registerResourceProvider(resource: Resource) {
        // Register as VS Code text document content provider
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
}

export function activate(context: vscode.ExtensionContext) {
    const extension = new VSCodeMCPExtension(context);
    context.subscriptions.push(extension);
}