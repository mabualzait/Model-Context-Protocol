# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.6 Deployment Considerations

from flask import Flask, request, jsonify

app = Flask(__name__)
host = MCPHost({})

@app.route('/sessions', methods=['POST'])
def create_session():
    """Create new MCP session"""
    data = request.json
    client_info = data.get("client_info", {})
    server_configs = data.get("server_configs", [])
    
    session_id = host.create_session(client_info, server_configs)
    return jsonify({"session_id": session_id})

@app.route('/sessions/<session_id>/messages', methods=['POST'])
def route_message(session_id):
    """Route message through session"""
    message = request.json
    
    try:
        response = host.route_message(session_id, message)
        return jsonify(response) if response else ("", 204)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/sessions/<session_id>', methods=['DELETE'])
def destroy_session(session_id):
    """Destroy session"""
    host.destroy_session(session_id)
    return ("", 204)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)