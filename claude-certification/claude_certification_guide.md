# 🎓 Claude Certified Architect – Foundations (CCA-F)
### Complete Exam Guide & Study Plan

---

## 📋 Exam Overview

| Detail | Info |
|---|---|
| **Certification Name** | Claude Certified Architect – Foundations (CCA-F) |
| **Issued By** | Anthropic (Official) |
| **Launched** | March 2026 |
| **Exam Type** | Proctored, Closed-Book, Scenario-Based |
| **Questions** | 60 multiple-choice / multi-select |
| **Duration** | 120 minutes |
| **Passing Score** | 720 / 1,000 |
| **Cost** | $99 per attempt (Free for first 5,000 partner employees) |
| **Availability** | Currently restricted to Claude Partner Network; general availability expected soon |

> [!IMPORTANT]
> The exam is **currently available only to employees of companies in the Claude Partner Network**. However, you can prepare now, as general availability is expected soon.

---

## 🗂️ Exam Format — How It Works

- You will be presented with **4 randomly selected scenarios** from a pool of **6 real-world scenarios**.
- Each scenario simulates a **production-grade enterprise challenge**.
- Questions test **architectural judgment**, not definition memorization.
- No AI tools, documentation, or external browser tabs are allowed.

### 🎭 Sample Exam Scenarios
1. **Customer Support Agent** — Design a multi-turn, stateful support bot
2. **Claude Code for CI/CD** — Automate code review pipelines
3. **Multi-Agent Research System** — Orchestrate hub-and-spoke agent networks
4. **Enterprise Document Processing** — Structured output at scale
5. **Long-Context Code Analysis** — Managing 200k+ token contexts
6. **Production Reliability & Fallback Design** — Human-in-the-loop systems

---

## 📊 Exam Domains & Weightings

| # | Domain | Weight | Key Topics |
|---|---|---|---|
| 1 | **Agentic Architecture & Orchestration** | **27%** | Agent SDK, multi-agent orchestration, hub-and-spoke models, task decomposition, lifecycle hooks, error propagation, `stop_reason` handling |
| 2 | **Claude Code Configuration & Workflows** | **20%** | `CLAUDE.md` file hierarchies, project setup, session continuity, CI/CD integration, plan mode, slash commands |
| 3 | **Prompt Engineering & Structured Output** | **20%** | Context engineering, JSON schemas, extraction patterns, few-shot prompting, validation-retry loops |
| 4 | **Tool Design & MCP Integration** | **18%** | Model Context Protocol (MCP) servers, tool boundaries, resources, custom tool implementation, tool composition |
| 5 | **Context Management & Reliability** | **15%** | Long-context handling, state management, fallback strategies, human-in-the-loop escalation, confidence calibration |

---

## 🧠 Domain Deep Dives

### Domain 1: Agentic Architecture & Orchestration (27%)
- Understand the **agentic loop lifecycle** — how Claude runs, uses tools, and ends turns
- Know `stop_reason` values: `tool_use` vs `end_turn` vs `max_tokens`
- **Hub-and-spoke vs sequential pipelines** — when to use each
- Multi-agent coordination patterns — orchestrator + sub-agents
- Error propagation between agents and proper retry logic
- Task decomposition strategies

### Domain 2: Claude Code Configuration & Workflows (20%)
- **`CLAUDE.md` file hierarchy** — global, project-level, and folder-level configs
- Setting up Claude Code for a repository
- **Session continuity** — maintaining context across sessions
- CI/CD integration patterns (GitHub Actions, etc.)
- Plan mode and slash commands usage

### Domain 3: Prompt Engineering & Structured Output (20%)
- **JSON Schema enforcement** for reliable structured outputs
- Few-shot prompting for consistency
- **Validation-retry loops** — detecting and fixing malformed output
- Context engineering (what to include vs. exclude)
- Extraction patterns from unstructured text

### Domain 4: Tool Design & MCP Integration (18%)
- **Model Context Protocol (MCP)** — server setup, resources, prompts, and tools
- Tool boundary design — when to split or combine tools
- Idempotent vs stateful tools
- Error handling in tool responses
- Custom MCP server implementation

### Domain 5: Context Management & Reliability (15%)
- Managing **200k+ token contexts** without loss of accuracy
- State management across long conversations
- **Fallback strategies** when Claude is uncertain
- **Human-in-the-loop** escalation design
- Confidence calibration patterns

---

## ⚠️ Common Anti-Patterns to Know

> [!WARNING]
> The exam specifically tests your ability to **identify anti-patterns** that cause production systems to fail.

- ❌ Not handling `tool_use` `stop_reason` properly (infinite loops)
- ❌ Poor context isolation in multi-agent systems
- ❌ Over-relying on a single monolithic agent instead of task decomposition
- ❌ Ignoring fallback and error propagation paths
- ❌ Missing validation-retry loops for structured output
- ❌ Not setting appropriate `max_tokens` limits
- ❌ Treating all tools as stateless when they're not

---

## 📚 Official Study Resources

| Resource | Link | Cost |
|---|---|---|
| **Anthropic Academy** | [academy.anthropic.com](https://www.anthropic.com/academy) | Free |
| Claude 101 Course | Part of Anthropic Academy | Free |
| Building with Claude API | Part of Anthropic Academy | Free |
| Intro to Model Context Protocol | Part of Anthropic Academy | Free |
| Official Exam Guide | Via Skilljar portal (partner access) | Free |

---

## 🔧 Third-Party Practice Resources

| Platform | Notes |
|---|---|
| **Udemy** | Practice tests mirroring the scenario-based format |
| **Tutorials Dojo** | CCA-F specific mock exams |
| **explainx.ai** | Practice question banks |
| **SkillCertPro** | Mock exams for CCA-F |
| **Medium / GitHub** | Community study guides and scenario walkthroughs |

---

## 🗺️ Recommended Study Plan (6–8 Weeks)

### Week 1–2: Foundations
- [ ] Complete **Claude 101** on Anthropic Academy
- [ ] Complete **Building with the Claude API**
- [ ] Read the official Claude API documentation
- [ ] Understand Messages API, roles, and `stop_reason`

### Week 3–4: Agentic & MCP
- [ ] Complete **Introduction to Model Context Protocol**
- [ ] Build a simple MCP server locally
- [ ] Implement a basic agentic loop with tool use
- [ ] Study multi-agent orchestration patterns

### Week 5: Claude Code & Prompt Engineering
- [ ] Set up Claude Code on a project
- [ ] Experiment with `CLAUDE.md` hierarchies
- [ ] Practice JSON schema-enforced structured outputs
- [ ] Build validation-retry loops

### Week 6: Context Management & Practice
- [ ] Study long-context best practices
- [ ] Design fallback and human-in-the-loop systems
- [ ] Take 2–3 full practice tests on Udemy/Tutorials Dojo
- [ ] Review all anti-patterns

### Week 7–8: Final Review
- [ ] Focus on weakest domain (use domain weights to prioritize)
- [ ] Re-read all anti-patterns
- [ ] Time yourself on practice tests (120 min = 2 min/question)
- [ ] Register for the exam when you score 80%+ on practice tests

---

## 💡 Key Tips from Exam Takers

> [!TIP]
> **Architectural judgment > definitions.** Knowing what MCP stands for is not enough — you must know *when* to use a multi-server MCP setup vs a single server.

1. **Focus on the "why"** — Every question will give you 4 plausible-looking answers. The right one is always the best *architectural decision* for the specific constraints.
2. **Know `stop_reason` cold** — This comes up repeatedly in agentic loop questions.
3. **6 months of hands-on experience** is the recommended baseline before sitting the exam.
4. **Scenario analysis practice** is more valuable than flashcards.
5. The gap between "I know what agents are" and "I can architect a production agent system" is where most candidates fail.

---

## 🔗 Quick Links

- 🌐 Official: [anthropic.com/academy](https://www.anthropic.com/academy)
- 📝 Exam Info: [claudecertifications.com](https://claudecertifications.com)
- 🛠️ Claude API Docs: [docs.anthropic.com](https://docs.anthropic.com)
- 🧩 MCP Docs: [modelcontextprotocol.io](https://modelcontextprotocol.io)
