# Claude Certification

Hands-on projects for the **Claude AI Engineer certification**, built with the Anthropic API.

---

## 📂 Structure

```
claude-certification/
├── main.py              # Entry point — starts the MCP CLI chat app
├── mcp_client.py        # MCP client (connects to MCP server, wraps tools/resources/prompts)
├── mcp_server.py        # MCP server (defines tools, resources, and prompts)
├── core/
│   ├── claude.py        # Anthropic API wrapper
│   ├── chat.py          # Chat session logic
│   ├── cli.py           # CLI app runner
│   ├── cli_chat.py      # CLI chat handler
│   └── tools.py         # Tool definitions
├── claude-code/
│   ├── README.md        # Claude Code usage notes
│   └── MCP.md           # MCP concepts reference
└── .env.example         # Points to root .env (secrets live at repo root)
```

---

## ⚙️ Setup

Secrets are managed at the **repo root** — no local `.env` needed here.

```bash
# From repo root — one-time setup
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and CLAUDE_MODEL in .env
```

---

## ▶️ Running

```bash
# From repo root
uv run claude-certification/main.py

# Or from inside this folder
cd claude-certification
uv run main.py
```

---

## 🏗️ Architecture

```
main.py
  └─ MCPClient  ──connects to──▶  mcp_server.py  (FastMCP server)
  └─ Claude     ──calls──────────▶ Anthropic API
  └─ CliApp     ──renders──────▶  Terminal UI
```

### MCP Features

| Feature | File | Status |
|---------|------|--------|
| `read_doc_contents` tool | `mcp_server.py` | ✅ Done |
| `edit_document` tool | `mcp_server.py` | ✅ Done |
| `docs://documents` resource | `mcp_server.py` | ✅ Done |
| `format` prompt | `mcp_server.py` | ✅ Done |
| Tool calling in client | `mcp_client.py` | ✅ Done |
