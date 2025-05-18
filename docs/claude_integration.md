# Claude Integration Guide for A2A MCP Server

## Overview

This guide explains how to connect Claude to your A2A MCP server, allowing Claude to use the server's functionality through a specialized endpoint.

## Setup Instructions

1. Start your MCP server:
```bash
python -m mcp_server
```

2. The Claude integration endpoint is available at: `http://localhost:8080/claude`

## Using Claude with MCP Server

When interacting with Claude Desktop or Claude API, you can configure it to use your MCP server by adding the server URL to your configuration.

### Example for Claude Desktop

Paste this snippet into Claude Desktop to enable MCP integration:

```json
{
  "mcp_config": {
    "server_url": "http://localhost:8080/claude",
    "enable_streaming": true,
    "auth_token": "" 
  }
}
```

### API Request Format

If you're building an application that connects Claude with your MCP server, use this format:

```json
POST http://localhost:8080/claude
Content-Type: application/json

{
  "prompt": "Your message to Claude",
  "claude_id": "optional-claude-session-id",
  "stream": true 
}
```

## Response Format

### For non-streaming requests:

```json
{
  "task_id": "task-12345",
  "response": "Claude's response text",
  "status": "completed"
}
```

### For streaming requests:

The initial response will contain a stream URL:

```json
{
  "task_id": "task-12345",
  "stream_url": "/tasks/task-12345/stream",
  "status": "processing"
}
```

Then connect to the stream URL with Server-Sent Events (SSE) to receive real-time updates.

## Advanced Configuration

You can modify the Claude handler in `mcp_server/api/handlers/claude.py` to customize the integration with specific Claude features or authentication requirements.

## Troubleshooting

If you encounter issues:

1. Ensure your server is running and accessible
2. Check the server logs for error messages
3. Verify your request format matches the expected structure
4. Confirm any firewalls or security settings allow the connection