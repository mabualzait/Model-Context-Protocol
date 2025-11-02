# 📖 Chapter: Chapter 8: Integrating MCP into Applications
# 📖 Section: 8.3 Web Application Integration

from flask import Flask
from flask_socketio import SocketIO, emit
from mcp_host import MCPHost

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
host = MCPHost({})

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    # Create MCP session for client
    session_id = host.create_session(
        {"name": "websocket-client", "version": "1.0.0"},
        [{"transport": "stdio", "command": ["python", "-m", "filesystem-server"]}]
    )
    
    emit('session_created', {'session_id': session_id})

@socketio.on('mcp_request')
def handle_mcp_request(data):
    """Handle MCP request."""
    session_id = data['session_id']
    message = data['message']
    
    try:
        response = host.route_message(session_id, message)
        emit('mcp_response', response)
    except Exception as e:
        emit('mcp_error', {'error': str(e)})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    # Clean up sessions (implementation depends on session tracking)
    pass

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)