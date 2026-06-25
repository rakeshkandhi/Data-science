# Claude Code

## 1. Patterns

### 1.1 Named session resumption

- `claude --session-name "<name>"`
- Use it for work that you expect to pause and resume in the same thread.
- Keep the name stable for the task, not for the machine or the day.

## 2. Useful sources to include

### 2.1 Official Claude Code docs

- Overview: https://docs.anthropic.com/en/docs/claude-code/overview
- Memory and `CLAUDE.md`: https://docs.anthropic.com/en/docs/claude-code/memory
- Settings: https://docs.anthropic.com/en/docs/claude-code/settings
- Slash commands: https://docs.anthropic.com/en/docs/claude-code/slash-commands
- GitHub Actions: https://docs.anthropic.com/en/docs/claude-code/github-actions

### 2.2 Official Anthropic docs

- Messages API: https://docs.anthropic.com/en/api/messages
- Tool use: https://docs.anthropic.com/en/docs/tool-use
- Agents overview: https://docs.anthropic.com/en/docs/agents
- Prompt engineering: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- Structured outputs: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency
- Errors and rate limits: https://docs.anthropic.com/en/api/errors, https://docs.anthropic.com/en/api/rate-limits

### 2.3 MCP sources

- MCP introduction: https://modelcontextprotocol.io/introduction
- MCP architecture: https://modelcontextprotocol.io/docs/concepts/architecture
- MCP tools: https://modelcontextprotocol.io/docs/concepts/tools
- MCP resources: https://modelcontextprotocol.io/docs/concepts/resources
- MCP prompts: https://modelcontextprotocol.io/docs/concepts/prompts
- Python quickstart: https://modelcontextprotocol.io/quickstart/server

### 2.4 Local repo examples

- [`mcp_server.py`](../mcp_server.py) for tools, resources, and prompts
- [`mcp_client.py`](../mcp_client.py) for client-side tool and resource calls
- [`core/tools.py`](../core/tools.py) for tool execution and result shaping
- [`core/cli_chat.py`](../core/cli_chat.py) for prompt injection and resource lookup

## 3. Concepts to track

- Progressive summarization: keep a rolling summary as context grows, instead of replaying the full history.
- Speculative execution: branch on likely next steps, then keep the branch that matches reality.
- `context: fork` frontmatter: use explicit metadata to split one context into several task-specific tracks.
- Code generation with Claude Code: compare Skills vs `CLAUDE.md` scope, and use the narrower mechanism first when the rule is local.
- Iterative refinement: generate, review, revise, and re-run until the output stabilizes.
- `CLAUDE.md` configuration hierarchy: global, project, and folder scopes should be additive and specific.
- Self-critique step: use an evaluator-optimizer pass when the first draft is likely to miss constraints.
- Separation of concerns: keep orchestration, retrieval, editing, and review in separate layers.
- Rolling summary vs parallel extraction: summarize when the thread is growing; extract in parallel when you need multiple facts from the same source.

## 4. What to add next

- [`GAME_PLAN.md`](./GAME_PLAN.md) for the full anti-pattern and concept checklist.
- A short `CLAUDE.md` example showing global vs project vs folder scope.
- A `slash-commands.md` page with one or two practical commands.
- A `mcp-notes.md` page that maps your sample server to the MCP concepts.
- One worked example of a Claude Code workflow, from prompt to tool call to result.
