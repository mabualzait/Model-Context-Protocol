# 📖 Chapter: Chapter 6: The Host: Orchestrating MCP Sessions
# 📖 Section: 6.6 Production Deployment Strategies

from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import os

app = Flask(__name__)
host = MCPHost()

# Prometheus metrics
requests_total = Counter('mcp_host_requests_total', 'Total requests', ['method', 'status'])
request_duration = Histogram('mcp_host_request_duration_seconds', 'Request duration')
active_sessions = Gauge('mcp_host_active_sessions', 'Active sessions')

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest()

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "active_sessions": len(host.sessions),
        "uptime": time.time() - host.start_time
    })

@app.route('/ready')
def ready():
    """Readiness check endpoint."""
    # Check if host is ready to accept requests
    if host.is_ready():
        return jsonify({"status": "ready"}), 200
    else:
        return jsonify({"status": "not ready"}), 503

@app.route('/sessions', methods=['POST'])
def create_session():
    """Create new MCP session."""
    data = request.json
    
    try:
        session_id = host.create_session(
            data.get("client_info", {}),
            data.get("server_configs", [])
        )
        
        active_sessions.inc()
        
        return jsonify({"session_id": session_id}), 201
    except Exception as e:
        requests_total.labels(method="create_session", status="error").inc()
        return jsonify({"error": str(e)}), 400

@app.route('/sessions/<session_id>/messages', methods=['POST'])
def route_message(session_id):
    """Route message through session."""
    message = request.json
    
    start_time = time.time()
    try:
        response = host.route_message(session_id, message)
        
        method = message.get("method", "unknown")
        requests_total.labels(method=method, status="success").inc()
        request_duration.observe(time.time() - start_time)
        
        return jsonify(response) if response else ("", 204)
    except Exception as e:
        method = message.get("method", "unknown")
        requests_total.labels(method=method, status="error").inc()
        request_duration.observe(time.time() - start_time)
        
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.getenv("MCP_HOST_PORT", 5000))
    app.run(host='0.0.0.0', port=port)