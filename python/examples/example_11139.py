# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.3 Web Application Integration

from flask import Flask, request, jsonify
from mcp_host import MCPHost
import uuid

app = Flask(__name__)
host = MCPHost({})

@app.route('/api/mcp/sessions', methods=['POST'])
def create_session():
    """Create MCP session."""
    data = request.json
    client_info = data.get("client_info", {})
    server_configs = data.get("server_configs", [])
    
    session_id = host.create_session(client_info, server_configs)
    return jsonify({"session_id": session_id})

@app.route('/api/mcp/sessions/<session_id>/resources', methods=['GET'])
def list_resources(session_id):
    """List resources."""
    request_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "resources/list"
    }
    
    response = host.route_message(session_id, request_message)
    return jsonify(response["result"])

@app.route('/api/mcp/sessions/<session_id>/resources/<path:uri>', methods=['GET'])
def read_resource(session_id, uri):
    """Read resource."""
    request_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "resources/read",
        "params": {"uri": f"file://{uri}"}
    }
    
    response = host.route_message(session_id, request_message)
    return jsonify(response["result"])

@app.route('/api/mcp/sessions/<session_id>/tools', methods=['POST'])
def call_tool(session_id):
    """Call tool."""
    data = request.json
    request_message = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": data["name"],
            "arguments": data.get("arguments", {})
        }
    }
    
    response = host.route_message(session_id, request_message)
    return jsonify(response["result"])

@app.route('/api/mcp/sessions/<session_id>', methods=['DELETE'])
def destroy_session(session_id):
    """Destroy session."""
    host.destroy_session(session_id)
    return ("", 204)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)