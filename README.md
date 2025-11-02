# Model Context Protocol - Code Examples

**Companion code repository for "Model Context Protocol: Solving the N×M Integration Problem in AI Applications"**

This repository contains all the code examples, implementations, and complete applications discussed in the MCP technical book.

🔗 **Book Repository:** Private (book content not included in this public repository)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (for Python examples)
- Node.js 16+ and npm (for TypeScript examples)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/mabualzait/Model-Context-Protocol.git
cd Model-Context-Protocol

# Python setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# TypeScript setup
cd typescript
npm install
npm run build
cd ..
```

## 📚 Repository Structure

```
Model-Context-Protocol/
├── python/          # Python implementations
│   ├── servers/     # MCP server implementations
│   ├── clients/    # MCP client implementations
│   ├── hosts/      # MCP host implementations
│   └── utils/      # Utility classes and helpers
├── typescript/      # TypeScript implementations
├── examples/        # Complete application examples by chapter
├── tests/          # Test suites
├── configs/        # Configuration files (Docker, Kubernetes, etc.)
└── docs/           # Additional documentation
```

## 📖 Chapter Mapping

### Part I: Foundations

**Chapter 1: Introduction to Model Context Protocol**
- `python/servers/filesystem_server.py` - File system MCP server
- `python/servers/database_server.py` - Database integration example

**Chapter 2: The Architecture of MCP**
- `python/utils/jsonrpc.py` - JSON-RPC 2.0 implementation
- `python/utils/session_state.py` - Session state management
- `python/utils/error_handling.py` - Error handling patterns

**Chapter 3: MCP in the Ecosystem**
- `typescript/src/hosts/claude-desktop-host.ts` - Claude Desktop host
- `typescript/src/hosts/vscode-host.ts` - VS Code integration

### Part II: Core Components

**Chapter 4: MCP Servers**
- `python/servers/` - All server implementations
  - `filesystem_server.py`
  - `database_server.py`
  - `api_server.py`
  - `composed_server.py`
  - `async_server.py`
  - `stateful_server.py`

**Chapter 5: MCP Clients**
- `python/clients/` - All client implementations
  - `basic_client.py`
  - `multi_server_client.py`
  - `resilient_client.py`
  - `cached_client.py`
  - `production_client.py`

**Chapter 6: The Host**
- `python/hosts/` - All host implementations
  - `basic_host.py`
  - `load_balanced_host.py`
  - `ha_host.py`
  - `event_driven_host.py`

### Part III: Practical Implementation

**Chapter 7: Building Your First MCP Server**
- `examples/chapter-07/file-management-server/` - Complete production server

**Chapter 8: Integrating MCP into Applications**
- `examples/chapter-08/vscode-extension/` - VS Code extension
- `examples/chapter-08/react-app/` - React application
- `examples/chapter-08/nextjs-api/` - Next.js API routes

**Chapter 9: Advanced MCP Patterns**
- `examples/chapter-09/multi-server-setup/` - Multi-server architecture
- `examples/chapter-09/workflow-orchestrator/` - Workflow orchestration

### Part IV: Security and Operations

**Chapter 10-12:** Security, monitoring, and compliance examples
- Configuration files in `configs/`
- Security implementations in server/client examples

### Part V: Advanced Topics

**Chapter 13: Multi-Agent Systems**
- `python/hosts/multi_agent_host.py` - Multi-agent orchestrator

**Chapter 14: Enterprise Integration**
- `python/servers/enterprise_database_server.py` - Enterprise database
- `python/servers/legacy_adapter.py` - Legacy system adapter

**Chapter 15: The Future of MCP**
- Example implementations demonstrating future patterns

## 🧪 Running Examples

### Run a Server

```bash
# File system server
python python/servers/filesystem_server.py --root-path /path/to/directory

# Database server
python python/servers/database_server.py --connection-string postgresql://user:pass@localhost/db
```

### Run a Client

```bash
# Basic client
python python/clients/basic_client.py --server-command python python/servers/filesystem_server.py

# Production client
python python/clients/production_client.py --config configs/client-config.json
```

### Run Tests

```bash
# Python tests
pytest tests/python/

# TypeScript tests
cd typescript
npm test
```

## 📝 Code Reference Format

Each code example in the book includes a reference like:

```python
# 📁 File: python/servers/filesystem_server.py
# 📖 Chapter 1, Section 1.9: Use Case 1
# 🔗 GitHub: https://github.com/mabualzait/Model-Context-Protocol/blob/main/python/servers/filesystem_server.py
```

## 🔧 Configuration

### Claude Desktop Configuration

Edit `configs/claude-desktop-config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["/path/to/Model-Context-Protocol/python/servers/filesystem_server.py"],
      "env": {}
    }
  }
}
```

### Docker Deployment

```bash
docker-compose -f configs/docker-compose.yml up
```

### Kubernetes Deployment

```bash
kubectl apply -f configs/kubernetes/
```

## 📚 Additional Resources

- **Setup Guide:** `docs/setup-guide.md`
- **Architecture Documentation:** `docs/architecture.md`
- **Contributing Guidelines:** `docs/contributing.md`

## 🤝 Contributing

Contributions are welcome! Please see `docs/contributing.md` for guidelines.

## 📄 License

This code repository is provided as-is for educational purposes. See `LICENSE` file for details.

## 💡 Using the Code

1. **Learning:** Follow along with the book using these examples
2. **Experimenting:** Modify and test different configurations
3. **Building:** Use as a foundation for your own MCP projects
4. **Teaching:** Use in courses or tutorials about MCP

## 🔗 Links

- **MCP Specification:** https://modelcontextprotocol.io
- **Official MCP SDK:** https://github.com/modelcontextprotocol/servers

## 📧 Support

For issues related to:
- **Code examples:** Open an issue in this repository
- **Book content:** Contact the publisher
- **MCP protocol:** Visit the official MCP documentation

---

**Note:** This repository is a companion to the book. The code is organized by chapter and includes both simple examples for learning and complete production-ready implementations.

