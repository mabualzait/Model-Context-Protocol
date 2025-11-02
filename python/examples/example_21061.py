# 📖 Chapter: Appendices
# 📖 Section: E.3 Performance Tuning Guide

# Use connection pooling
from mcp.pool import ConnectionPool

pool = ConnectionPool(
    endpoint="http://localhost:8080",
    max_connections=10,
    max_idle=5
)

# Reuse connections
with pool.get_connection() as conn:
    result = conn.call_tool("tool_name", {})