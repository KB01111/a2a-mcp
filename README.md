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

### Docker Deployment (Local or VPS)

```bash
# Build the Docker image
docker build -t mcp-server .

# Run locally
docker run -p 8080:8080 mcp-server

# For VPS deployment
docker run -d --restart unless-stopped -p 8080:8080 mcp-server
```

### VPS Deployment Guide

1. SSH into your VPS: `ssh user@your-vps-ip`
2. Install Docker if not installed:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. Clone the repository: `git clone https://github.com/KB01111/a2a-mcp.git`
4. Navigate to directory: `cd a2a-mcp`
5. Build and run the container:
   ```bash
   docker build -t mcp-server .
   docker run -d --restart unless-stopped -p 8080:8080 mcp-server
   ```
6. Verify it's running: `docker ps`
7. Test the endpoint: `curl http://localhost:8080/health`

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
- [VPS Deployment Guide](docs/vps_deployment.md) - Detailed instructions for deploying to a VPS

## Production Considerations

When deploying to a VPS for production:

- Use a proper domain name with SSL/TLS (see VPS deployment guide)
- Enable authentication by setting environment variables
- Configure monitoring and regular backups
- Consider using Docker Compose for more complex deployments
- Use a container orchestration platform (like Kubernetes) for high-availability scenarios