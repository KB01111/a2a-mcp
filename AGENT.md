# Agent Guidelines for a2a-mcp

## Commands
- Build: `python -m mcp_server`
- Test: `pytest`
- Lint: `flake8 --max-line-length=88 --extend-ignore=E203`
- Format: `black .`
- Docker Build: `docker build -t mcp-server .`

## Code Style Guidelines
- **Naming**: PascalCase for classes, snake_case for functions/variables
- **Formatting**: Black formatter with 88-character line limit
- **Imports**: Group: 1) standard library, 2) third-party packages, 3) local imports
- **Type Hints**: Use Python type hints (PEP 484) for all function parameters and returns
- **Async/Await**: Use async/await patterns with proper exception handling
- **Error Handling**: Use explicit error handling with structured error responses
- **Comments**: Docstrings using triple quotes with param/return documentation

## Architecture
- JSON-RPC 2.0 over HTTP with SSE streaming support
- Modular components following the architecture in the context guide
- Task-based lifecycle management with proper state transitions
- RESTful API for agent discovery and management

## A2A Protocol
- Follow A2A protocol standards from Google (github.com/google/A2A)
- Implementation uses Task, Message, and Part as core data models