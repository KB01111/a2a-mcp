# A2A Message Control Protocol (MCP) Server

A high-performance implementation of the Agent-to-Agent (A2A) protocol developed by Google, enabling communication and interoperability between independent AI agent systems.

## Features

- JSON-RPC 2.0 over HTTP(S) with streaming (SSE) support
- Agent discovery and management via Agent Cards
- Robust task lifecycle management
- Cross-framework agent communication support
- Direct Claude AI integration
- Secure authentication and authorization
- Containerized deployment with Kubernetes support

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/KB01111/a2a-mcp.git
cd a2a-mcp

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
python -m mcp_server
```

### Docker Deployment

```bash
docker build -t mcp-server .
docker run -p 8080:8080 mcp-server
```

## Claude AI Integration

This MCP server includes a dedicated endpoint for Claude AI integration. To connect Claude to this server, use:

```json
{
  "mcp_config": {
    "server_url": "http://localhost:8080/claude",
    "enable_streaming": true
  }
}
```

See [Claude Integration Guide](docs/claude_integration.md) for detailed instructions.

## Documentation

- [A2A Protocol Repository](https://github.com/google/A2A) - Official A2A protocol specification
- [Claude Integration Guide](docs/claude_integration.md) - Using this MCP server with Claude