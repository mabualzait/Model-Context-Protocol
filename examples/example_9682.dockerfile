# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.6 Deployment and Distribution

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENTRYPOINT ["python", "-m", "my_mcp_server.server"]