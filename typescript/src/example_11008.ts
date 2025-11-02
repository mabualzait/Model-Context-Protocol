# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.2 IDE Integrations

import * as vscode from 'vscode';
import { MCPClient } from '@modelcontextprotocol/client';

export function activate(context: vscode.ExtensionContext) {
    const mcpClient = new MCPClient({
        command: 'python',
        args: ['-m', 'filesystem-server'],
    });
    
    mcpClient.connect().then(() => {
        // Register MCP-based code actions
        const codeActionProvider = new MCPCodeActionProvider(mcpClient);
        context.subscriptions.push(
            vscode.languages.registerCodeActionsProvider('*', codeActionProvider)
        );
        
        // Register MCP-based commands
        context.subscriptions.push(
            vscode.commands.registerCommand('mcp.readFile', async (uri: vscode.Uri) => {
                const content = await mcpClient.readResource(`file://${uri.fsPath}`);
                return content;
            })
        );
    });
}

class MCPCodeActionProvider implements vscode.CodeActionProvider {
    constructor(private mcpClient: MCPClient) {}
    
    provideCodeActions(
        document: vscode.TextDocument,
        range: vscode.Range,
        context: vscode.CodeActionContext
    ): vscode.ProviderResult<vscode.CodeAction[]> {
        const actions: vscode.CodeAction[] = [];
        
        // Use MCP tools for code actions
        const tools = this.mcpClient.listTools();
        
        for (const tool of tools) {
            if (tool.name === 'code_review') {
                const action = new vscode.CodeAction(
                    `Review with ${tool.name}`,
                    vscode.CodeActionKind.QuickFix
                );
                action.command = {
                    command: 'mcp.callTool',
                    title: 'Review Code',
                    arguments: [tool.name, { code: document.getText() }]
                };
                actions.push(action);
            }
        }
        
        return actions;
    }
}