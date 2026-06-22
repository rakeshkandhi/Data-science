# ⚡ CCA-F 2-Day Intensive Study Plan
### Claude Certified Architect – Foundations Exam Crash Course

> [!CAUTION]
> This is a high-intensity crash plan. Study 10–12 hours per day. Prioritize high-weight domains (27% + 20% + 20% = 67% of the exam). Skip deep dives on 15% domain if time runs short.

---

## 🗓️ DAY 1 — Core Architecture & Agentic Systems
**Goal: Master the top 3 domains = 67% of the exam**

---

### 🌅 Morning Block (9:00 AM – 12:00 PM) | 3 hrs
**Domain 1: Agentic Architecture & Orchestration (27%) ← HIGHEST PRIORITY**

#### 9:00 – 10:00 AM — The Agentic Loop
- [ ] How Claude processes a turn (input → thinking → tool calls → response)
- [ ] Understand **`stop_reason`** values and what to do for each:

| `stop_reason` | Meaning | What to Do |
|---|---|---|
| `end_turn` | Claude finished naturally | Done — return to user |
| `tool_use` | Claude wants to call a tool | Execute tool, send result back |
| `max_tokens` | Hit token limit | Handle gracefully, ask Claude to continue |
| `stop_sequence` | Hit a custom stop string | Process accordingly |

- [ ] **Anti-pattern to memorize**: NOT handling `tool_use` → infinite loop or dropped tool calls

#### 10:00 – 11:00 AM — Multi-Agent Patterns
- [ ] **Hub-and-Spoke**: Central orchestrator + specialized sub-agents
  - ✅ Use when: parallel tasks, specialized expertise needed
  - ❌ Avoid when: tasks are sequential and tightly coupled
- [ ] **Sequential Pipeline**: Agent A → Agent B → Agent C
  - ✅ Use when: tasks must happen in order
  - ❌ Avoid when: tasks are independent (wasted latency)
- [ ] **Task decomposition**: Break complex tasks into atomic sub-tasks
- [ ] Error propagation — sub-agent fails → orchestrator must handle, retry, or escalate

#### 11:00 AM – 12:00 PM — Agent Lifecycle & State
- [ ] Session state management across agent turns
- [ ] Lifecycle hooks: on_start, on_tool_call, on_error, on_end
- [ ] How to pass context between agents safely
- [ ] **Quick Quiz yourself**: Draw a multi-agent architecture for a research system from memory

---

### 🍽️ Lunch Break (12:00 PM – 1:00 PM) | 1 hr
- Light review of morning notes
- Watch a YouTube overview of Claude agentic systems

---

### ☀️ Afternoon Block 1 (1:00 PM – 3:00 PM) | 2 hrs
**Domain 3: Prompt Engineering & Structured Output (20%)**

#### 1:00 – 1:45 PM — JSON Schema & Structured Output
- [ ] How to enforce JSON output using system prompts + schemas
- [ ] **Validation-retry loop pattern**:
  ```
  1. Ask Claude to output JSON
  2. Validate against schema
  3. If invalid → send error + ask Claude to fix
  4. Retry up to N times → escalate if still failing
  ```
- [ ] Extraction patterns from unstructured documents

#### 1:45 – 2:30 PM — Context Engineering & Few-Shot
- [ ] What to include vs. exclude in context (relevance > volume)
- [ ] Few-shot examples: how many (3–5 optimal), format matters
- [ ] Role/persona prompts for consistency
- [ ] Chain-of-thought prompting for complex reasoning tasks

#### 2:30 – 3:00 PM — Anti-Patterns in Prompting
- [ ] ❌ Overloading system prompt with contradictory instructions
- [ ] ❌ No validation → malformed JSON in production
- [ ] ❌ No few-shot → inconsistent output format
- [ ] ❌ Including irrelevant context → dilutes attention

---

### ☀️ Afternoon Block 2 (3:00 PM – 5:30 PM) | 2.5 hrs
**Domain 2: Claude Code Configuration & Workflows (20%)**

#### 3:00 – 4:00 PM — CLAUDE.md Hierarchy
- [ ] **Three levels of CLAUDE.md**:
  ```
  ~/.claude/CLAUDE.md          ← Global (applies everywhere)
  /project/CLAUDE.md           ← Project-level (overrides global)
  /project/subfolder/CLAUDE.md ← Folder-level (most specific wins)
  ```
- [ ] What to put in CLAUDE.md: coding standards, project context, file structure, dos and don'ts
- [ ] More specific = higher priority (folder > project > global)

#### 4:00 – 4:45 PM — Claude Code Workflows
- [ ] **Plan Mode**: Claude proposes a plan before executing — use for risky operations
- [ ] **Slash Commands**: `/review`, `/fix`, `/test`, custom commands
- [ ] Session continuity — how Claude Code maintains context across sessions
- [ ] CI/CD integration — GitHub Actions calling Claude Code for automated review

#### 4:45 – 5:30 PM — CI/CD & Automation Patterns
- [ ] Code review pipeline: PR opened → Claude reviews → comments posted
- [ ] Test generation pipeline: Claude writes tests based on code changes
- [ ] Anti-pattern: ❌ Running Claude in CI without a `max_tokens` budget → runaway costs
- [ ] Best practice: ✅ Scope Claude Code tasks narrowly in automation

---

### 🌆 Evening Block (6:00 PM – 8:30 PM) | 2.5 hrs
**Domain 4: Tool Design & MCP Integration (18%)**

#### 6:00 – 7:00 PM — MCP Fundamentals
- [ ] **MCP = Model Context Protocol** — standard for connecting Claude to external systems
- [ ] 3 MCP primitives:
  | Primitive | Purpose | Example |
  |---|---|---|
  | **Tools** | Claude can call these | `search_database()`, `send_email()` |
  | **Resources** | Read-only data Claude can access | Files, DB records, docs |
  | **Prompts** | Reusable prompt templates | Stored system prompts |
- [ ] MCP Server vs MCP Client architecture
- [ ] When to use 1 MCP server vs multiple (separate by domain/security boundary)

#### 7:00 – 7:45 PM — Tool Design Principles
- [ ] **Idempotent tools** (safe to retry) vs **stateful tools** (dangerous to retry)
- [ ] Tool boundary design:
  - ✅ One tool = one responsibility
  - ❌ Don't make a "do everything" mega-tool
- [ ] Always return structured error responses from tools
- [ ] Tool description quality matters — Claude reads it to decide when to use the tool

#### 7:45 – 8:30 PM — Anti-Patterns in Tool Design
- [ ] ❌ Not handling tool errors → Claude gets confused, loops
- [ ] ❌ Stateful tools without idempotency keys → duplicate side effects
- [ ] ❌ Vague tool descriptions → Claude misuses the tool
- [ ] ❌ Too many tools at once → Claude gets overwhelmed (best: <10 tools per turn)

---

### 🌙 Night Review (9:00 PM – 10:00 PM) | 1 hr
- [ ] Re-read all your Day 1 notes
- [ ] Write out the 5 domains + weights from memory
- [ ] Quiz: For each anti-pattern you learned — what's the correct pattern?
- [ ] Get 8 hours of sleep — memory consolidation is critical!

---

## 🗓️ DAY 2 — Reliability, Practice & Exam Strategy
**Goal: Complete Domain 5, do practice tests, lock in exam strategy**

---

### 🌅 Morning Block (8:00 AM – 10:00 AM) | 2 hrs
**Domain 5: Context Management & Reliability (15%)**

#### 8:00 – 9:00 AM — Long Context & State Management
- [ ] Claude supports up to **200k tokens** — but quality degrades near limits
- [ ] **Lost-in-the-middle problem**: Claude pays less attention to content in the middle of long contexts → put important info at the beginning OR end
- [ ] State management patterns:
  - External memory (database) for persistent state
  - Summarization to compress old context
  - Sliding window — drop oldest context as new arrives

#### 9:00 – 10:00 AM — Reliability & Fallback Design
- [ ] **Human-in-the-loop escalation**: Define confidence thresholds — if Claude is uncertain, escalate to human
- [ ] Fallback strategies:
  - Retry with simplified prompt
  - Fall back to a smaller, faster model
  - Return a safe default response
- [ ] Confidence calibration — ask Claude to rate its confidence; use that signal
- [ ] Circuit breaker pattern for agentic systems (stop retrying after N failures)

---

### ☀️ Morning Block 2 (10:00 AM – 12:00 PM) | 2 hrs
**Full Domain Review + Anti-Pattern Master List**

#### 10:00 – 11:00 AM — Master Anti-Pattern Review

| Domain | Top Anti-Pattern | Correct Pattern |
|---|---|---|
| Agentic | Not checking `stop_reason` | Always branch on `stop_reason` |
| Agentic | Monolithic single agent | Decompose into specialized agents |
| Claude Code | No `CLAUDE.md` config | Define standards in CLAUDE.md hierarchy |
| Prompt Eng | No validation loop | Validate JSON → retry on failure |
| MCP/Tools | Vague tool descriptions | Write precise, specific tool descriptions |
| MCP/Tools | Mega-tools | One tool = one responsibility |
| Context | Critical info in the middle | Put key info at start or end |
| Reliability | No fallback | Always design fallback + escalation |

#### 11:00 AM – 12:00 PM — Scenario Practice
- [ ] **Scenario 1**: Design a customer support agent (what agents? what tools? what fallback?)
- [ ] **Scenario 2**: Multi-agent research system (hub-and-spoke or sequential? why?)
- [ ] **Scenario 3**: CI/CD code review (CLAUDE.md setup? slash commands? cost guard?)
- [ ] For each scenario, practice eliminating wrong answers by spotting anti-patterns

---

### 🍽️ Lunch Break (12:00 PM – 1:00 PM)

---

### ☀️ Afternoon Block (1:00 PM – 4:00 PM) | 3 hrs
**Practice Tests**

- [ ] **1:00 – 2:00 PM** — Take Practice Test 1 (Udemy / Tutorials Dojo / explainx.ai)
  - Time yourself strictly: 60 questions in 60 minutes (save time for review)
- [ ] **2:00 – 2:30 PM** — Review every wrong answer. For each: WHY was the right answer better?
- [ ] **2:30 – 3:30 PM** — Take Practice Test 2
- [ ] **3:30 – 4:00 PM** — Review wrong answers again. Note patterns in mistakes.

> [!TIP]
> If you're scoring below 70% on practice tests, spend more time on Domain 1 (Agentic, 27%) — it's the biggest lever.

---

### 🌆 Evening Block (4:00 PM – 6:00 PM) | 2 hrs
**Weak Area Targeted Review**

- [ ] Look at which domain you got the most questions wrong
- [ ] Re-read those notes
- [ ] Do 15–20 targeted practice questions on just that domain

---

### 🌙 Final Review (7:00 PM – 9:00 PM) | 2 hrs
**Lock In Everything**

#### Quick-Reference Cheat Sheet (memorize this):

```
DOMAINS & WEIGHTS:
  1. Agentic Architecture     → 27% ← MOST IMPORTANT
  2. Claude Code Workflows    → 20%
  3. Prompt Engineering       → 20%
  4. Tool Design & MCP        → 18%
  5. Context & Reliability    → 15%

STOP_REASON VALUES:
  end_turn     → Claude is done, return to user
  tool_use     → Execute tool, send result back (LOOP BACK!)
  max_tokens   → Handle gracefully

MCP PRIMITIVES:
  Tools → Claude calls these (actions)
  Resources → Claude reads these (data)
  Prompts → Reusable templates

CLAUDE.MD PRIORITY:
  Folder > Project > Global

VALIDATION-RETRY LOOP:
  Generate → Validate → If fail: retry with error → N times → Escalate

CONTEXT RULE:
  Put critical info at START or END (not middle)

HUB-AND-SPOKE → Parallel tasks, specialized agents
SEQUENTIAL    → Ordered dependent tasks
```

- [ ] Sleep by 10:00 PM — your brain needs it!

---

## 📅 Exam Day Checklist

### Before the Exam
- [ ] Eat a proper meal
- [ ] Have water nearby
- [ ] Stable internet connection
- [ ] Quiet room (it's proctored!)
- [ ] Valid ID ready
- [ ] Close all other browser tabs

### During the Exam — Strategy
1. **Read the scenario first**, understand the constraints (latency? cost? accuracy?)
2. **Eliminate anti-patterns** — at least 1-2 answers will be obvious wrong patterns
3. **The "most architecturally sound" answer** wins — not the "simplest" answer
4. **Flag uncertain questions** and come back (don't waste time)
5. **Budget**: 120 min ÷ 60 questions = 2 min/question max
6. If two answers look right — pick the one that **handles failure/edge cases** better

### Question Answering Framework
```
Step 1: What is the constraint? (cost / latency / reliability / scale)
Step 2: Which architecture matches those constraints?
Step 3: Does any answer have an anti-pattern? Eliminate it.
Step 4: Which remaining answer is more production-grade?
```

---

## 🔗 Resources to Use RIGHT NOW

| Resource | What to Do |
|---|---|
| [Anthropic Docs](https://docs.anthropic.com) | Read: Messages API, Tool Use, Agentic Patterns |
| [MCP Docs](https://modelcontextprotocol.io) | Read: Overview + Quickstart |
| [Anthropic Academy](https://www.anthropic.com/academy) | Watch: Claude 101, Building with Claude API |
| [Udemy Practice Tests](https://udemy.com) | Search: "CCA-F practice test" |
| [explainx.ai](https://explainx.ai) | Practice question bank |
| [YouTube](https://youtube.com) | Search: "Claude agentic loop tutorial" |

---

> [!NOTE]
> **You've got this!** The exam rewards clear architectural thinking. When in doubt, always choose the answer that handles edge cases, has proper error handling, and avoids the obvious anti-patterns. Good luck! 🚀
