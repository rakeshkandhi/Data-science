# 📘 CCA-F Full Technical Documentation
### Claude Certified Architect – Foundations | Complete Study Reference with Sources

---

> **How to use this doc**: Read top-to-bottom for full coverage, or jump to the domain you're weak in. Every concept includes a source link. Code examples are production-grade patterns.

---

## 📑 Table of Contents

1. [Domain 1 — Agentic Architecture & Orchestration (27%)](#domain-1)
2. [Domain 2 — Claude Code Configuration & Workflows (20%)](#domain-2)
3. [Domain 3 — Prompt Engineering & Structured Output (20%)](#domain-3)
4. [Domain 4 — Tool Design & MCP Integration (18%)](#domain-4)
5. [Domain 5 — Context Management & Reliability (15%)](#domain-5)
6. [Master Anti-Patterns Reference](#anti-patterns)
7. [Sources & Further Reading](#sources)

---

<a id="domain-1"></a>
## 🧠 Domain 1 — Agentic Architecture & Orchestration
### Weight: 27% | Priority: HIGHEST

---

### 1.1 What is an Agentic Loop?

An **agentic loop** is the core execution cycle where Claude iteratively sends/receives API calls, uses tools, and reasons until a task is complete. It is the backbone of all agent-based Claude applications.

**Source:** [Anthropic Docs — Tool Use Overview](https://docs.anthropic.com/en/docs/tool-use)

#### The 4-Step Loop:

```
┌─────────────────────────────────────────────────────────┐
│  1. SEND   → Send messages array to Claude API          │
│  2. CHECK  → Inspect stop_reason in the response        │
│  3. ACT    → If tool_use: execute tool, append result   │
│  4. REPEAT → Send updated messages back to Claude       │
└─────────────────────────────────────────────────────────┘
```

#### Code Example — Basic Agentic Loop (Python):

```python
import anthropic

client = anthropic.Anthropic()
messages = []

def run_agent(user_input: str):
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            tools=my_tools,
            messages=messages
        )

        # CRITICAL: Always branch on stop_reason
        if response.stop_reason == "end_turn":
            # Claude is done — return final response
            return response.content[0].text

        elif response.stop_reason == "tool_use":
            # Claude wants to call a tool
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})
            # Loop back ↑

        elif response.stop_reason == "max_tokens":
            # Handle gracefully — ask Claude to continue
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": "Please continue."})
```

**Source:** [claudecertificationguide.com — Agentic Loop](https://claudecertificationguide.com)

---

### 1.2 `stop_reason` — Complete Reference

> [!IMPORTANT]
> The `stop_reason` field is the **single most tested concept** on the exam. Never use natural language parsing to determine when to stop — always use `stop_reason`.

| `stop_reason`   | Meaning                                            | Required Action                                      |
| --------------- | -------------------------------------------------- | ---------------------------------------------------- |
| `end_turn`      | Claude completed naturally                         | Return response to user. Loop ends.                  |
| `tool_use`      | Claude wants to invoke a tool                      | Execute all tool(s), append `tool_result`, loop back |
| `max_tokens`    | Response hit the `max_tokens` limit                | Handle gracefully — send "continue" or summarize     |
| `stop_sequence` | Hit a custom stop string you defined               | Process as needed for your use case                  |
| `pause_turn`    | Server-side tool is running (Anthropic handles it) | Wait — Anthropic will resume automatically           |

**Source:** [Anthropic API Reference — Messages](https://docs.anthropic.com/en/api/messages)

#### ❌ Anti-Pattern:
```python
# WRONG — Never parse text to decide when to stop
if "I'm done" in response.content[0].text:
    break
```

#### ✅ Correct Pattern:
```python
# CORRECT — Always use stop_reason
if response.stop_reason == "end_turn":
    break
```

---

### 1.3 Multi-Agent Orchestration Patterns

#### Pattern A: Hub-and-Spoke (Parallel)

```
           ┌──────────────────┐
           │   ORCHESTRATOR   │  ← Receives task, decomposes it
           │     (Claude)     │
           └────────┬─────────┘
          ┌─────────┼─────────┐
          ▼         ▼         ▼
    ┌──────────┐ ┌──────┐ ┌──────────┐
    │ Agent A  │ │Agent │ │ Agent C  │
    │(Search)  │ │  B   │ │(Analyst) │
    └──────────┘ └──────┘ └──────────┘
```

**When to use:**
- ✅ Tasks can be done **in parallel**
- ✅ Each agent has a **specialized role**
- ✅ You want to minimize total latency

**When NOT to use:**
- ❌ Tasks must happen in strict order
- ❌ Output of one agent is input to the next

**Source:** [explainx.ai — Multi-Agent Orchestration](https://explainx.ai)

---

#### Pattern B: Sequential Pipeline

```
  Input → [Agent A: Research] → [Agent B: Write] → [Agent C: Review] → Output
```

**When to use:**
- ✅ Tasks are **tightly coupled** — each depends on the previous
- ✅ Clear sequence of stages with defined handoffs
- ✅ You need strict ordering for correctness

**When NOT to use:**
- ❌ Tasks are independent (wastes latency by forcing serialization)

---

### 1.4 Task Decomposition

Break complex tasks into **atomic, verifiable sub-tasks**:

```
Complex Task: "Write a market analysis report"
          ↓
Decomposition:
  1. Gather company data     (Agent A: Search specialist)
  2. Analyze financials      (Agent B: Finance specialist)
  3. Identify competitors    (Agent A: Search specialist)
  4. Synthesize findings     (Orchestrator: Writer)
  5. Format report           (Orchestrator: Formatter)
```

**Key principle:** Each sub-task should have:
- A **clear input**
- A **verifiable output**
- A **single responsibility**

**Source:** [panaversity.org — CCA-F Study Guide](https://panaversity.org)

---

### 1.5 Error Propagation in Multi-Agent Systems

```python
# Orchestrator handling sub-agent failure
async def orchestrate(task):
    try:
        result = await sub_agent_a.run(task)
    except AgentError as e:
        # Don't silently fail — propagate with context
        if e.is_retryable:
            result = await sub_agent_a.run(task)  # Retry once
        elif e.needs_human:
            return escalate_to_human(task, reason=str(e))
        else:
            return fallback_response(task)
```

**Rules:**
1. Sub-agent failures **must be caught** at the orchestrator level
2. Always implement **retry logic** for transient failures
3. Define a **maximum retry count** (avoid infinite loops)
4. Escalate to human if retries are exhausted

---

### 1.6 Anthropic's Core Agentic Workflows (2026 Updated)

Anthropic distinguishes between **Workflows** (predefined code paths orchestrating LLMs and tools) and **Agents** (LLMs dynamically directing their own processes).

**Source:** [Anthropic Research — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

#### The 5 Core Patterns:
1. **Prompt Chaining**: Decomposing a task into a sequence of steps, where each LLM call processes the output of the previous one. (Trade latency for higher accuracy on fixed subtasks).
2. **Routing**: Classifying an input and directing it to a specialized downstream task or model (e.g., routing complex questions to Claude 4.5 Sonnet, simple ones to Claude 4.5 Haiku).
3. **Parallelization**: 
   - *Sectioning*: Breaking tasks into independent subtasks run in parallel (e.g., guardrails).
   - *Voting*: Running the same task multiple times to get diverse outputs and consensus.
4. **Orchestrator-Workers**: A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes results. Ideal for complex tasks where you can't predict subtasks in advance (like coding across multiple files).
5. **Evaluator-Optimizer**: One LLM call generates a response, another provides evaluation and feedback in a loop. Great for tasks with clear evaluation criteria (e.g., literary translation, complex search).

---

### 1.7 Workflow Enforcement & Handoff

> [!IMPORTANT]
> A prompt is a **sign** (probabilistic — works most of the time); programmatic enforcement is a **lock** (deterministic — works every time). The stakes of the action dictate which you must use.

**Source:** [anthropiccertifications.com — Workflow Enforcement & Handoff](https://www.anthropiccertifications.com/courses/claude-certified-architect-foundations/workflow-enforcement-and-handoff)

#### The Enforcement Spectrum
| Requirement | Stakes | Use |
|---|---|---|
| Consistent date formatting | Low — a miss is harmless | Prompt / few-shot examples |
| Friendly, on-brand tone | Low | Prompt |
| Verify identity before refund | High — money at risk | Programmatic enforcement (Code) |
| Run AML check before transfer | High — compliance | Programmatic enforcement (Code) |

#### The Prerequisite Gate — Building the "Lock"
A prerequisite gate is code that refuses to let a downstream action run until a required earlier step has completed. Since you run the `tool_use` branch, you can enforce sequence logic outside of Claude's prompt:

```python
verified_ids = set()

def on_tool_call(name, args):
    if name == "get_customer" and args.get("verified"):
        verified_ids.add(args["customer_id"])
    
    # The Gate: downstream action impossible until prerequisite met
    if name == "process_refund" and args.get("customer_id") not in verified_ids:
        return block("Refund blocked: customer identity not verified this session")
    return allow()
```

#### Handling Multi-Concern Requests
When users bundle issues (e.g., "late order AND double charge"), the agent must:
1. **Decompose** the message into distinct concerns.
2. **Investigate** each concern (ideally in parallel) using shared context.
3. **Synthesize** a single, unified resolution response.

#### Structured Handoffs to Humans
When escalating to a human, the agent must pass the context. A bare "escalating to a human" forces the user to repeat themselves.

```python
# CORRECT: Pass the summary, tool results, and context
def handoff_to_human(session):
    context_summary = summarize_session(session)
    return escalate(
        reason="Policy exception requested",
        summary=context_summary,
        transcript=session.messages
    )
```

---

<a id="domain-2"></a>
## 💻 Domain 2 — Claude Code Configuration & Workflows
### Weight: 20% | Priority: HIGH

---

### 2.1 CLAUDE.md — The Configuration Hierarchy

Claude Code uses an **additive, hierarchical** system for `CLAUDE.md` files. All applicable files are loaded — they stack on top of each other, with more specific files taking priority on conflicts.

**Source:** [panaversity.org — CLAUDE.md Hierarchy](https://panaversity.org) | [Anthropic Docs — Claude Code](https://docs.anthropic.com/en/docs/claude-code)

#### The 3 Levels:

```
~/.claude/CLAUDE.md                  ← Level 1: GLOBAL (personal, never shared)
                                       Applies to ALL projects on your machine
/my-project/CLAUDE.md                ← Level 2: PROJECT (committed to git, shared with team)
                                       Applies to entire project
/my-project/packages/api/CLAUDE.md   ← Level 3: DIRECTORY (most specific, highest priority)
                                       Applies only within that subdirectory
```

#### Priority Rule:
```
Directory CLAUDE.md > Project CLAUDE.md > Global CLAUDE.md
```

#### What goes where:

| Level                             | Content                                                               |
| --------------------------------- | --------------------------------------------------------------------- |
| **Global** (`~/.claude/`)         | Personal preferences, formatting style, communication tone            |
| **Project** (`./CLAUDE.md`)       | Tech stack, architecture overview, coding standards, test conventions |
| **Directory** (`./packages/api/`) | Module-specific rules (e.g., "always use async/await in this module") |

#### Special Files:
- `CLAUDE.local.md` — Personal overrides **not committed to git** (in `.gitignore`), for project-level personal notes
- `@` references — Import shared files: e.g., `@~/.claude/code-standards.md`

**Source:** [Medium — CLAUDE.md Deep Dive](https://medium.com) | [panaversity.org](https://panaversity.org)

---

### 2.2 What to Write in CLAUDE.md

```markdown
# Project: MyApp

## Tech Stack
- Backend: FastAPI (Python 3.11)
- Frontend: React 18 + TypeScript
- Database: PostgreSQL + SQLAlchemy

## Architecture
- REST API with versioning (/api/v1/)
- Service layer between routes and DB
- Always use dependency injection

## Coding Standards
- Use type hints on ALL functions
- Write docstrings for public methods
- Max function length: 50 lines

## Testing
- pytest for unit tests
- Always mock external API calls
- Minimum 80% coverage

## Do NOT
- Commit secrets or API keys
- Use print() — use logging instead
- Modify migration files directly
```

---

### 2.3 Claude Code Workflows

#### Plan Mode
Before executing risky operations, Claude proposes a plan and waits for approval:

```bash
# Activate plan mode for a risky refactor
claude --plan "Refactor the authentication module to use JWT"

# Claude outputs:
# 1. I will modify auth/views.py to add JWT decode logic
# 2. I will update auth/models.py to add token_blacklist table
# 3. I will update tests/test_auth.py
# Proceed? [y/n]
```

**When to use Plan Mode:**
- ✅ Database schema changes
- ✅ Deleting or moving files
- ✅ Modifying CI/CD configuration
- ❌ Not needed for simple bug fixes or comments

---

#### CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude review \
            --diff $(git diff origin/main...HEAD) \
            --max-tokens 2000 \
            --output github-comment
```

**Anti-pattern:** Running Claude in CI without `max_tokens` limits → runaway API costs

**Source:** [Anthropic Docs — Claude Code CI/CD](https://docs.anthropic.com)

---

### 2.4 Session Continuity

Claude Code maintains state across sessions using:
1. **`CLAUDE.md`** — Static project knowledge (always loaded)
2. **`.claude/sessions/`** — Session history and checkpoints
3. **Tool memory** — Results from previous tool calls in the same session

```bash
# Resume a previous session
claude --resume session-id-abc123

# Start fresh but with project context
claude --reset-history
```

---

<a id="domain-3"></a>
## ✍️ Domain 3 — Prompt Engineering & Structured Output
### Weight: 20% | Priority: HIGH

---

### 3.1 Structured Output — Native JSON Schema

Claude (Sonnet 4.5+, Opus 4.1+) supports **native structured outputs** via constrained decoding, guaranteeing schema compliance.

**Source:** [Anthropic Docs — Structured Outputs](https://docs.anthropic.com/en/docs/structured-outputs) | [thomas-wiegold.com](https://thomas-wiegold.com)

```python
import anthropic
from pydantic import BaseModel
from typing import List

class ProductReview(BaseModel):
    sentiment: str          # "positive" | "negative" | "neutral"
    score: int              # 1-10
    key_points: List[str]   # Up to 5 bullet points
    recommend: bool

client = anthropic.Anthropic()

# Method 1: Native structured output (recommended for supported models)
response = client.messages.parse(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Analyze this review: {review_text}"}],
    response_format=ProductReview   # Pydantic model → JSON schema automatically
)

# response.parsed is a ProductReview object — guaranteed valid
print(response.parsed.sentiment)
print(response.parsed.score)
```

---

### 3.2 Validation-Retry Loop

For older models or complex schemas where native output isn't available:

```python
import json
import jsonschema

REVIEW_SCHEMA = {
    "type": "object",
    "required": ["sentiment", "score", "key_points", "recommend"],
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "score": {"type": "integer", "minimum": 1, "maximum": 10},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "recommend": {"type": "boolean"}
    }
}

def extract_with_retry(text: str, max_retries: int = 3) -> dict:
    messages = [
        {
            "role": "user",
            "content": f"Analyze this review and respond ONLY with valid JSON: {text}"
        }
    ]

    for attempt in range(max_retries):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            messages=messages
        )

        raw = response.content[0].text.strip()

        try:
            # Parse JSON
            parsed = json.loads(raw)
            # Validate against schema
            jsonschema.validate(parsed, REVIEW_SCHEMA)
            return parsed  # ✅ Valid — return it

        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            # Feed error back to Claude for self-correction
            messages.append({"role": "assistant", "content": raw})
            messages.append({
                "role": "user",
                "content": f"Your response had this error: {e}. Please fix and return only valid JSON."
            })

    # All retries exhausted — escalate
    raise ValueError(f"Failed to get valid JSON after {max_retries} attempts")
```

**Source:** [GitHub — Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) | [thomas-wiegold.com](https://thomas-wiegold.com)

---

### 3.3 Few-Shot Prompting

Use 2–4 high-quality examples to demonstrate the desired output format and logic.

**Source:** [nanonets.com — Few-Shot Prompting Guide](https://nanonets.com) | [YouTube — Anthropic Few-Shot Tutorial](https://youtube.com)

```python
system_prompt = """
You are a customer intent classifier. Classify the user's message into one of:
BILLING, TECHNICAL, GENERAL, COMPLAINT.

Examples:
---
User: "My invoice shows a charge I don't recognize"
Classification: BILLING

User: "The app crashes every time I open it"
Classification: TECHNICAL

User: "What are your business hours?"
Classification: GENERAL

User: "This is completely unacceptable, I've been waiting 3 weeks"
Classification: COMPLAINT
---

Respond ONLY with the classification label. No explanation.
"""
```

**The 2-4 Example Rule:**
- **2-4 examples** → optimal performance
- **< 2** → model may not pick up the pattern
- **> 6** → risk of overfitting to example style

---

### 3.4 Context Engineering

**Principle:** *Relevance beats volume.* Including irrelevant context dilutes Claude's attention.

**Source:** [Medium — Context Engineering for Claude](https://medium.com)

```
❌ BAD: Dump everything into the system prompt (10,000 tokens of docs)
✅ GOOD: Include only what Claude needs for THIS specific task

Strategy:
  1. Static context  → CLAUDE.md / System prompt (always relevant)
  2. Dynamic context → RAG: retrieve only relevant chunks
  3. Tool results    → Append as needed during the conversation
```

#### The "Write, Select, Compress" Framework:
| Strategy     | How                                         | When                           |
| ------------ | ------------------------------------------- | ------------------------------ |
| **Write**    | Store to files / memory (CLAUDE.md, DB)     | Persistent, reusable knowledge |
| **Select**   | RAG — retrieve only relevant chunks         | Large knowledge bases          |
| **Compress** | Summarize old context, remove stale entries | Long-running conversations     |

---

### 3.5 XML Tags for Prompt Structure

Claude is trained to recognize XML tags as structural delimiters:

```python
system_prompt = """
You are a code reviewer. Your task is provided below.

<task_description>
Review the following Python function for bugs, security issues, and style violations.
</task_description>

<review_criteria>
1. Check for SQL injection vulnerabilities
2. Verify error handling
3. Ensure PEP-8 compliance
</review_criteria>

<output_format>
Return a JSON object with keys: "bugs", "security_issues", "style_violations"
Each key maps to a list of strings.
</output_format>
"""
```

**Source:** [Anthropic Docs — Prompt Engineering](https://docs.anthropic.com/en/docs/prompt-engineering)

---

<a id="domain-4"></a>
## 🔧 Domain 4 — Tool Design & MCP Integration
### Weight: 18% | Priority: MEDIUM-HIGH

---

### 4.1 Model Context Protocol (MCP) — Overview

MCP is an **open standard** (created by Anthropic) for connecting Claude to external data sources and systems. It provides a universal interface, so you build an MCP server once and it works with any MCP-compatible client.

**Source:** [modelcontextprotocol.io — Official Docs](https://modelcontextprotocol.io) | [GitHub — MCP Repository](https://github.com/modelcontextprotocol)

```
┌────────────────┐         MCP Protocol          ┌──────────────────┐
│  MCP Client    │ ◄──────────────────────────► │   MCP Server     │
│ (Claude / App) │                               │ (Your Backend)   │
└────────────────┘                               └──────────────────┘
```

---

### 4.2 The 3 MCP Primitives

**Source:** [modelcontextprotocol.io — Core Concepts](https://modelcontextprotocol.io/docs/concepts) | [dailydoseofds.com](https://dailydoseofds.com)

| Primitive     | Type                | Direction                      | Purpose                   | Example                                  |
| ------------- | ------------------- | ------------------------------ | ------------------------- | ---------------------------------------- |
| **Tools**     | Active / Executable | Claude calls → Server executes | Claude "does" things      | `search_database()`, `send_email()`      |
| **Resources** | Passive / Read-only | Client pulls → Server returns  | Claude "reads" data       | File contents, DB records, API responses |
| **Prompts**   | Templates           | Client selects                 | Reusable prompt templates | `debug_code`, `summarize_document`       |

#### Tools — Claude-initiated actions:
```python
# MCP Server definition (Python SDK)
from mcp.server import Server
from mcp.types import Tool

server = Server("my-backend")

@server.tool()
async def search_products(query: str, limit: int = 10) -> list[dict]:
    """
    Search the product catalog.
    
    Args:
        query: Search query string
        limit: Maximum number of results (1-100)
    
    Returns:
        List of matching products with id, name, price, stock
    """
    # Tool description above is what Claude reads to decide when to use it
    results = await db.search(query, limit=limit)
    return results
```

#### Resources — Read-only data:
```python
@server.resource("config://app-settings")
async def get_app_settings() -> str:
    """Read-only application configuration."""
    return json.dumps(load_config())
```

#### Prompts — Reusable templates:
```python
@server.prompt()
async def code_review_prompt(language: str, code: str) -> str:
    return f"Review this {language} code for bugs and security issues:\n\n{code}"
```

---

### 4.3 Tool Design Principles

**Source:** [Medium — Tool Design Best Practices](https://medium.com) | [claudecertificationguide.com](https://claudecertificationguide.com)

#### Principle 1: One Tool = One Responsibility
```python
# ❌ BAD — "god tool" that does everything
def manage_user(action, user_id, data=None):
    if action == "get":    return get_user(user_id)
    elif action == "update": return update_user(user_id, data)
    elif action == "delete": return delete_user(user_id)

# ✅ GOOD — separate tools with clear purpose
def get_user(user_id: str) -> dict: ...
def update_user(user_id: str, fields: dict) -> dict: ...
def delete_user(user_id: str) -> bool: ...
```

#### Principle 2: Write Precise Tool Descriptions
```python
# ❌ BAD — vague, Claude will misuse it
def search(q):
    """Search stuff."""

# ✅ GOOD — precise, Claude knows exactly when and how to use it
def search_customer_orders(
    customer_id: str,
    status: str = "all",  # "pending" | "shipped" | "delivered" | "all"
    limit: int = 20
) -> list[dict]:
    """
    Search orders for a specific customer.
    Use this when the user asks about their order history or order status.
    Returns: list of orders with fields: order_id, date, status, total, items
    Do NOT use for searching products — use search_products() for that.
    """
```

#### Principle 3: Idempotent vs Stateful Tools
| Type           | Definition                           | Example              | Retry Safe? |
| -------------- | ------------------------------------ | -------------------- | ----------- |
| **Idempotent** | Same result if called multiple times | `get_weather("NYC")` | ✅ Yes       |
| **Stateful**   | Each call has a side effect          | `send_email(...)`    | ❌ No        |

```python
# For stateful tools — use idempotency keys
def send_notification(user_id: str, message: str, idempotency_key: str) -> bool:
    """
    Sends a push notification. Use the idempotency_key to prevent duplicates
    if this tool is retried. Generate a unique key per logical operation.
    """
    if cache.exists(idempotency_key):
        return True  # Already sent — safe to return success
    
    result = push_service.send(user_id, message)
    cache.set(idempotency_key, True, ttl=3600)
    return result
```

---

### 4.4 MCP Server Architecture — When to Split

```
❌ BAD — One giant MCP server for everything:
  my-mega-server: [50 tools for HR + Finance + Engineering + Sales]

✅ GOOD — Separate servers by domain/security boundary:
  hr-server:          [employee_lookup, org_chart, leave_balance]
  finance-server:     [invoice_lookup, expense_report, budget_query]
  engineering-server: [deploy_app, get_logs, run_tests]
```

**When to split MCP servers:**
- Different **security scopes** (finance data vs engineering data)
- Different **team ownership**
- Different **authentication requirements**
- Approaching **10+ tools** in a single server (cognitive load)

**Source:** [modelcontextprotocol.io — Architecture](https://modelcontextprotocol.io)

---

### 4.5 Tool Error Handling

Always return structured errors — never throw raw exceptions back to Claude:

```python
@server.tool()
async def get_customer(customer_id: str) -> dict:
    try:
        customer = await db.get_customer(customer_id)
        if not customer:
            # Return structured "not found" — don't raise
            return {
                "error": True,
                "error_type": "NOT_FOUND",
                "message": f"Customer {customer_id} not found",
                "suggestion": "Try searching with search_customers() first"
            }
        return {"error": False, "data": customer}
    except DatabaseError as e:
        return {
            "error": True,
            "error_type": "DATABASE_ERROR",
            "message": "Database temporarily unavailable",
            "retryable": True
        }
```

---

<a id="domain-5"></a>
## 🛡️ Domain 5 — Context Management & Reliability
### Weight: 15% | Priority: MEDIUM

---

### 5.1 Long Context Management

Claude supports up to **200k tokens** (Sonnet/Opus models), but quality degrades near limits.

**Source:** [Anthropic Docs — Long Context](https://docs.anthropic.com/en/docs/long-context) | [vincentvandeth.nl](https://vincentvandeth.nl)

#### The "Lost in the Middle" Problem:
Claude pays **less attention** to content in the middle of very long prompts.

```
┌───────────────────────────────────────────────────────────────┐
│ BEGINNING OF CONTEXT         │ MIDDLE          │ END OF CONTEXT│
│ ← High attention             │ Low attention   │ High attention→│
│ Put: Critical instructions   │ Avoid: Key data │ Put: Examples  │
└───────────────────────────────────────────────────────────────┘
```

**Source:** [Medium — Lost in the Middle Research](https://medium.com)

#### Memory Tier Architecture:
```
Tier 1: IN-CONTEXT (active, fast)
  → Current conversation, recent tool results
  → Limit: ~65-70% of max context window

Tier 2: EXTERNAL MEMORY (retrieved, slower)
  → Vector database (semantic search)
  → Relational DB (structured facts)
  → Use RAG to fetch relevant chunks

Tier 3: PERSISTENT STORAGE (static, always available)
  → CLAUDE.md files
  → System prompts
  → Configuration files
```

**Source:** [Medium — Memory Tiers for AI Agents](https://medium.com)

---

### 5.2 Context Budget Management

Never use the full context window — set a **conservative effective limit**:

```python
MAX_CONTEXT_TOKENS = 200_000          # Actual model limit
EFFECTIVE_LIMIT = 130_000            # Use only 65% — leave room

def check_context_budget(messages: list) -> bool:
    """Returns True if we should compress context."""
    estimated_tokens = estimate_tokens(messages)
    
    if estimated_tokens > EFFECTIVE_LIMIT:
        return True  # Time to compress
    return False

def compress_context(messages: list) -> list:
    """Summarize old messages to free up context."""
    if len(messages) < 10:
        return messages  # Nothing to compress
    
    # Keep system prompt + last 5 messages intact
    old_messages = messages[1:-5]
    recent_messages = messages[-5:]
    
    # Summarize the old messages
    summary = summarize_conversation(old_messages)
    
    return [
        messages[0],  # System prompt
        {"role": "user", "content": f"[Previous conversation summary]: {summary}"},
        {"role": "assistant", "content": "Understood, continuing from there."},
        *recent_messages
    ]
```

**Source:** [GitHub — Context Management Patterns](https://github.com) | [sfeir.com](https://sfeir.com)

---

### 5.3 Fallback & Reliability Patterns

**Source:** [claudecertificationguide.com](https://claudecertificationguide.com) | [dev.to — Reliability Patterns](https://dev.to)

#### Circuit Breaker Pattern:

```python
class AgentCircuitBreaker:
    def __init__(self, failure_threshold=3, reset_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.state = "CLOSED"  # CLOSED | OPEN | HALF_OPEN
        self.last_failure_time = None

    async def call(self, agent_fn, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                # Circuit is open — fail fast, don't hit Claude
                return self.fallback_response()

        try:
            result = await agent_fn(*args, **kwargs)
            self.reset()  # Success — reset failures
            return result
        except Exception as e:
            self.record_failure()
            if self.failures >= self.threshold:
                self.state = "OPEN"
                self.last_failure_time = time.time()
            raise

    def fallback_response(self):
        return {"error": True, "message": "Service temporarily unavailable. Please try again later."}
```

---

### 5.4 Human-in-the-Loop (HITL) — Tiered Escalation

**Source:** [kili-technology.com — HITL Patterns](https://kili-technology.com) | [dev.to](https://dev.to)

```
┌──────────────────────────────────────────────────────────────┐
│                    TIERED REVIEW SYSTEM                       │
├────────────────────┬─────────────────────────────────────────┤
│ Tier 1: AUTOMATED  │ Routine, low-risk tasks                 │
│                    │ Claude acts autonomously                 │
│                    │ e.g., FAQ answers, status checks        │
├────────────────────┼─────────────────────────────────────────┤
│ Tier 2: HUMAN-ON-  │ Medium complexity or risk               │
│ THE-LOOP           │ Claude drafts → human approves          │
│                    │ e.g., customer refunds, config changes  │
├────────────────────┼─────────────────────────────────────────┤
│ Tier 3: HUMAN-IN-  │ High risk, edge cases, low confidence  │
│ THE-LOOP           │ Routed directly to human specialist     │
│                    │ e.g., legal issues, large transactions  │
└────────────────────┴─────────────────────────────────────────┘
```

#### Confidence-Based Routing:

```python
async def route_request(user_request: str) -> Response:
    # Step 1: Ask Claude to assess its confidence
    assessment = await claude.complete(
        f"On a scale of 1-10, how confident are you in handling this autonomously? "
        f"Request: {user_request}\n"
        f"Respond with JSON: {{\"confidence\": 8, \"reason\": \"...\"}}"
    )
    
    confidence = assessment["confidence"]
    
    if confidence >= 8:
        # Tier 1: Handle autonomously
        return await claude.handle(user_request)
    
    elif confidence >= 5:
        # Tier 2: Claude drafts, human reviews
        draft = await claude.draft(user_request)
        return await human_review_queue.submit(draft)
    
    else:
        # Tier 3: Route directly to human
        return await human_specialist_queue.escalate(user_request, reason=assessment["reason"])
```

---

### 5.5 State Management Patterns

```python
# External state management — don't rely on in-context memory for persistence
class AgentStateManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def save_state(self, session_id: str, state: dict):
        """Persist state externally — survives context resets."""
        await self.redis.setex(
            f"agent:state:{session_id}",
            3600,  # 1 hour TTL
            json.dumps(state)
        )

    async def load_state(self, session_id: str) -> dict:
        """Reload state at the start of each session."""
        data = await self.redis.get(f"agent:state:{session_id}")
        return json.loads(data) if data else {}
```

---

<a id="anti-patterns"></a>
## ⛔ Master Anti-Patterns Reference

> [!WARNING]
> The exam specifically tests your ability to **identify** these anti-patterns in scenario questions. Study them by name.

| #   | Anti-Pattern                     | Domain | What Goes Wrong                                       | Fix                                     |
| --- | -------------------------------- | ------ | ----------------------------------------------------- | --------------------------------------- |
| 1   | **Ignoring `stop_reason`**       | D1     | Infinite loops, dropped tool results                  | Always branch on `stop_reason`          |
| 2   | **Monolithic Agent**             | D1     | Poor scalability, single point of failure             | Decompose into specialized agents       |
| 3   | **No Error Propagation**         | D1     | Silent failures in multi-agent chains                 | Catch, log, retry, or escalate          |
| 4   | **Wrong Orchestration Pattern**  | D1     | Unnecessary latency (serial when parallel possible)   | Match pattern to task dependencies      |
| 5   | **Missing CLAUDE.md**            | D2     | Claude lacks project context, inconsistent output     | Define project standards in CLAUDE.md   |
| 6   | **No `max_tokens` in CI**        | D2     | Runaway API costs in automation                       | Always set budget limits                |
| 7   | **No Validation Loop**           | D3     | Malformed JSON breaks production pipeline             | Implement parse → validate → retry      |
| 8   | **Context Dumping**              | D3     | Diluted attention, irrelevant output                  | Use RAG for selective context injection |
| 9   | **No Examples**                  | D3     | Inconsistent output format                            | Use 2-4 few-shot examples               |
| 10  | **God Tool (Mega-Tool)**         | D4     | Claude can't decide when to use it, broad permissions | One tool = one responsibility           |
| 11  | **Vague Tool Descriptions**      | D4     | Claude misuses or ignores the tool                    | Write precise, specific descriptions    |
| 12  | **Retrying Stateful Tools**      | D4     | Duplicate side effects (double-charge, double-email)  | Use idempotency keys                    |
| 13  | **Too Many Tools at Once**       | D4     | Claude gets overwhelmed, picks wrong tool             | Limit to <10 tools per invocation       |
| 14  | **Key Info in Middle**           | D5     | Lost in the middle — Claude misses critical info      | Put key info at start or end            |
| 15  | **Using 100% of Context Window** | D5     | Degraded quality, no room for tool results            | Limit to 65-70% of max                  |
| 16  | **No Fallback Design**           | D5     | System fails hard on errors                           | Design fallback + escalation paths      |
| 17  | **No Human Escalation Path**     | D5     | AI handles things it shouldn't                        | Implement tiered HITL review            |

---

<a id="sources"></a>
## 📚 Sources & Further Reading

### Official Anthropic Resources
| Resource               | URL                                                                                                    | Topics Covered             |
| ---------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------- |
| Anthropic Docs (Main)  | [docs.anthropic.com](https://docs.anthropic.com)                                                       | All domains                |
| Messages API Reference | [docs.anthropic.com/en/api/messages](https://docs.anthropic.com/en/api/messages)                       | stop_reason, API format    |
| Tool Use Guide         | [docs.anthropic.com/en/docs/tool-use](https://docs.anthropic.com/en/docs/tool-use)                     | Domain 1 & 4               |
| Prompt Engineering     | [docs.anthropic.com/en/docs/prompt-engineering](https://docs.anthropic.com/en/docs/prompt-engineering) | Domain 3                   |
| Claude Code Docs       | [docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)               | Domain 2                   |
| Long Context Guide     | [docs.anthropic.com/en/docs/long-context](https://docs.anthropic.com/en/docs/long-context)             | Domain 5                   |
| Structured Outputs     | [docs.anthropic.com/en/docs/structured-outputs](https://docs.anthropic.com/en/docs/structured-outputs) | Domain 3                   |
| Anthropic Academy      | [anthropic.com/academy](https://www.anthropic.com/academy)                                             | All domains (free courses) |
| Anthropic Cookbook     | [github.com/anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook)           | Code examples              |

### MCP Resources
| Resource           | URL                                                                                    | Topics Covered            |
| ------------------ | -------------------------------------------------------------------------------------- | ------------------------- |
| MCP Official Docs  | [modelcontextprotocol.io](https://modelcontextprotocol.io)                             | Domain 4 (primary)        |
| MCP GitHub         | [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)             | SDKs, examples            |
| MCP Concepts Guide | [modelcontextprotocol.io/docs/concepts](https://modelcontextprotocol.io/docs/concepts) | Tools, Resources, Prompts |

### Exam-Specific Resources
| Resource                      | URL                                                          | Topics Covered          |
| ----------------------------- | ------------------------------------------------------------ | ----------------------- |
| CCA-F Exam Guide              | [claudecertifications.com](https://claudecertifications.com) | Exam format, domains    |
| Panaversity Study Guide       | [panaversity.org](https://panaversity.org)                   | All domains (deep dive) |
| Tutorials Dojo Practice Tests | [tutorialsdojo.com](https://tutorialsdojo.com)               | Practice exams          |
| explainx.ai Question Bank     | [explainx.ai](https://explainx.ai)                           | Practice questions      |
| SkillCertPro Mock Tests       | [skillcertpro.com](https://skillcertpro.com)                 | Mock exams              |
| Udemy CCA-F Course            | [udemy.com](https://udemy.com)                               | Full course + practice  |

### Technical Deep Dives
| Resource                    | URL                                                | Topics Covered |
| --------------------------- | -------------------------------------------------- | -------------- |
| Medium — Agentic Loop       | [medium.com](https://medium.com)                   | Domain 1       |
| nanonets.com Few-Shot Guide | [nanonets.com](https://nanonets.com)               | Domain 3       |
| kili-technology HITL        | [kili-technology.com](https://kili-technology.com) | Domain 5       |
| dev.to Reliability Patterns | [dev.to](https://dev.to)                           | Domain 5       |
| dailydoseofds.com MCP       | [dailydoseofds.com](https://dailydoseofds.com)     | Domain 4       |

---

## ⚡ Quick-Reference Exam Cheat Sheet

```
╔══════════════════════════════════════════════════════════╗
║              CCA-F QUICK REFERENCE                       ║
╠══════════════════════════════════════════════════════════╣
║ DOMAINS (by weight):                                     ║
║   D1: Agentic Architecture        27%  ← TOP PRIORITY   ║
║   D2: Claude Code & Workflows     20%                   ║
║   D3: Prompt Engineering          20%                   ║
║   D4: Tool Design & MCP           18%                   ║
║   D5: Context & Reliability       15%                   ║
╠══════════════════════════════════════════════════════════╣
║ STOP_REASON:                                             ║
║   end_turn   → Done, return to user                     ║
║   tool_use   → Execute tool, loop back                  ║
║   max_tokens → Handle gracefully                        ║
╠══════════════════════════════════════════════════════════╣
║ MCP PRIMITIVES:                                          ║
║   Tools      → Claude calls (actions/side-effects)      ║
║   Resources  → Claude reads (read-only data)            ║
║   Prompts    → Reusable templates                       ║
╠══════════════════════════════════════════════════════════╣
║ CLAUDE.MD PRIORITY:                                      ║
║   Directory > Project > Global (all additive)           ║
╠══════════════════════════════════════════════════════════╣
║ ORCHESTRATION:                                           ║
║   Hub-Spoke  → Parallel, specialized agents             ║
║   Sequential → Ordered, dependent tasks                 ║
╠══════════════════════════════════════════════════════════╣
║ CONTEXT RULES:                                           ║
║   - Critical info: START or END (never middle)          ║
║   - Use only 65-70% of max context window               ║
║   - Compress old context before hitting limits          ║
╠══════════════════════════════════════════════════════════╣
║ VALIDATION LOOP:                                         ║
║   Generate → Validate → Error→retry → N fails→escalate  ║
╚══════════════════════════════════════════════════════════╝
```

---

*Last updated: June 2026 | Based on CCA-F exam guide (claudecertifications.com) and official Anthropic documentation*
