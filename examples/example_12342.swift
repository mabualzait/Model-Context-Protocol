# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.9 Mobile Application Integration

import Foundation
import Network

class MCPClient {
    private let session = URLSession.shared
    private let baseURL: URL
    private var requestID: Int = 0
    
    init(baseURL: URL) {
        self.baseURL = baseURL
    }
    
    func initialize() async throws -> InitResult {
        let request = try createRequest(
            method: "initialize",
            params: InitParams(
                protocolVersion: "2024-11-05",
                capabilities: [:],
                clientInfo: ClientInfo(name: "ios-app", version: "1.0.0")
            )
        )
        
        let (data, _) = try await session.data(for: request)
        let response = try JSONDecoder().decode(JSONRPCResponse<InitResult>.self, from: data)
        
        return response.result
    }
    
    func listTools() async throws -> [Tool] {
        let request = try createRequest(method: "tools/list", params: [:])
        let (data, _) = try await session.data(for: request)
        let response = try JSONDecoder().decode(JSONRPCResponse<ToolListResult>.self, from: data)
        
        return response.result.tools
    }
    
    func callTool(name: String, arguments: [String: Any]) async throws -> ToolCallResult {
        let request = try createRequest(
            method: "tools/call",
            params: [
                "name": name,
                "arguments": arguments
            ]
        )
        
        let (data, _) = try await session.data(for: request)
        let response = try JSONDecoder().decode(JSONRPCResponse<ToolCallResult>.self, from: data)
        
        return response.result
    }
    
    private func createRequest(method: String, params: [String: Any]) throws -> URLRequest {
        var request = URLRequest(url: baseURL.appendingPathComponent("mcp"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        requestID += 1
        let jsonrpcRequest = JSONRPCRequest(
            jsonrpc: "2.0",
            id: requestID,
            method: method,
            params: params
        )
        
        request.httpBody = try JSONEncoder().encode(jsonrpcRequest)
        return request
    }
}

// Usage in SwiftUI
struct MCPView: View {
    @State private var client: MCPClient?
    @State private var tools: [Tool] = []
    
    var body: some View {
        List(tools) { tool in
            Button(tool.name) {
                Task {
                    try? await client?.callTool(tool.name, arguments: [:])
                }
            }
        }
        .onAppear {
            Task {
                client = MCPClient(baseURL: URL(string: "https://mcp-server.example.com")!)
                try? await client?.initialize()
                tools = try await client?.listTools() ?? []
            }
        }
    }
}