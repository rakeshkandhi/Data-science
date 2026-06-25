# MCP

## Core concepts

- Tools: actions Claude can call.
- Resources: read-only data Claude can fetch.
- Prompts: reusable templates that guide a task.

## Best sources

- Introduction: https://modelcontextprotocol.io/introduction
- Architecture: https://modelcontextprotocol.io/docs/concepts/architecture
- Tools: https://modelcontextprotocol.io/docs/concepts/tools
- Resources: https://modelcontextprotocol.io/docs/concepts/resources
- Prompts: https://modelcontextprotocol.io/docs/concepts/prompts
- Server quickstart: https://modelcontextprotocol.io/quickstart/server
- Client quickstart: https://modelcontextprotocol.io/quickstart/client

## Local examples

- [`mcp_server.py`](../mcp_server.py) shows one tool, one resource, and one prompt pattern.
- [`mcp_client.py`](../mcp_client.py) shows how a client discovers and calls MCP capabilities.
