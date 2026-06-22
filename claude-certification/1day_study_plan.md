# 🚨 CCA-F 1-Day EXTREME Crash Course Study Plan
> **Status:** Code Red. You have 24 hours. We are dropping everything except the highest ROI (Return on Investment) topics. 
> **Goal:** Pass the Claude Certified Architect - Foundations (CCA-F) exam.

## ⚖️ The "Cheat Code" Strategy
1. **Forget memorizing syntax.** The exam tests architectural judgment.
2. **Focus on Domain 1 (27%) and Domain 3 (20%)** — these two alone are nearly half the exam.
3. **Use the free [anthropiccertifications.com](https://www.anthropiccertifications.com) course** as your primary weapon.
4. **Master the Anti-Patterns:** The exam loves testing you on *what not to do*.

---

## 📅 The 14-Hour Execution Plan

### 🌅 MORNING: The Core Engine (4 Hours)
**Focus: Domain 1 (Agentic Architecture - 27%) & Domain 4 (Tool Design/MCP - 18%)**

* **08:00 - 09:30 | The Agentic Loop & Orchestration**
  * Read docs: `stop_reason` is king (branch on `tool_use`, `end_turn`, `max_tokens`).
  * Read [Anthropic's Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — memorize the 5 workflows (Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer).
  * *Lesson to skim:* 1.1 through 1.4 on anthropiccertifications.com.
* **09:30 - 10:30 | Workflow Enforcement**
  * The "Sign vs. Lock" rule: Financial/Security = Code (Lock). Tone/Format = Prompt (Sign).
  * Prerequisite gates (blocking execution in code, not prompts).
* **10:30 - 12:00 | Tools & MCP**
  * Tools = Claude calls (actions). Resources = Claude reads (data). Prompts = Templates.
  * Understand the difference between Server tools and Client tools.

### ☀️ MIDDAY: Claude Code & Prompting (3 Hours)
**Focus: Domain 2 (Claude Code - 20%) & Domain 3 (Prompting - 20%)**

* **12:30 - 14:00 | Claude Code Rules**
  * The CLAUDE.md Hierarchy: Directory > Project > Global (additive).
  * When to use `--plan` mode (database schema, risky refactors).
  * Remember that `.claude/sessions/` keeps state.
* **14:00 - 15:30 | Prompt Engineering & Structured Output**
  * Focus on Native JSON schema vs. manual parsing.
  * Few-shot prompting and using `<xml>` tags to isolate contexts.

### 🌇 AFTERNOON: Reliability & Context (2 Hours)
**Focus: Domain 5 (Context Management & Reliability - 15%)**

* **15:30 - 17:00 | Context & Escalation**
  * The golden rule of context: Key info goes at the START or END, never the middle.
  * Keep context usage below 70% of the max window.
  * Human-in-the-Loop (HITL): Tier 1 (Automated) -> Tier 2 (Draft/Approve) -> Tier 3 (Direct to human).
* **17:00 - 17:30 | 🛑 Anti-Pattern Review**
  * Open `cca_f_full_documentation.md` and read the **Master Anti-Patterns** table 3 times. 

### 🌙 EVENING: Practice & Simulation (5 Hours)
**Focus: Testing and Filling Gaps**

* **18:30 - 20:30 | Mock Exam 1**
  * Go to [anthropiccertifications.com/exam](https://www.anthropiccertifications.com/exam).
  * Take a full mock exam under timed conditions. Do not look up answers.
* **20:30 - 21:30 | The Gap Analysis**
  * Review *every single question* you got wrong. Find the concept in your docs and write it down.
* **21:30 - 23:30 | Mock Exam 2 & Final Review**
  * Take a second mock exam. Your score should jump by at least 15-20%.
  * Read the cheat sheet section of `cca_f_full_documentation.md` one last time before sleeping.

---

## ⚡ The 5-Minute "In the Exam Room" Checklist
If you blank out during the exam, remember these absolute truths:
1. **Never parse text to stop an agent.** Always check `stop_reason`.
2. **If stakes are high (money/data), pick the code answer.** Prompts cannot guarantee safety.
3. **Claude Code files stack.** Directory `CLAUDE.md` overrides Project `CLAUDE.md`.
4. **Tools should do one thing.** Mega-tools ("God tools") are an anti-pattern.
5. **Always pass context to a human.** A blind handoff is a failed handoff.

Good luck. You have exactly what you need to pass.
