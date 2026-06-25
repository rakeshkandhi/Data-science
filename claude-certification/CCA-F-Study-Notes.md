# CCA-F Exam — Personal Pattern & Trap Notes

> Built entirely from the questions you worked through. This is your "how I actually think through a question" playbook, not a doc dump. Practice score: **841/1000 (passed, 720 needed)**. Weakest scenario: **Multi-Agent Research System (67%)**.

---

## PART 1 — HOW TO APPROACH ANY QUESTION

A repeatable 4-step process. Run it in order, every time.

### Step 1 — Identify the actual problem (the mechanism, not the topic)
Don't ask "what topic is this?" Ask **"what specific thing is broken, and what number/behaviour needs to move?"**

- "Investigation time per finding" is a different problem from "too many findings."
- "Inconsistent output format" is different from "Claude lacks code context."
- "Miscategorising cases" is different from "uncertain about its own output."

The wrong answer is usually right for a *neighbouring* problem. Pin the exact mechanism first.

### Step 2 — Extract the constraints (these silently eliminate options)
Scan for constraint phrases. Any option that violates one is **dead on arrival**, no matter how elegant:

| Constraint phrase | What it eliminates |
|---|---|
| "stakeholders rejected filtering" | Any option that filters/suppresses |
| "without adding human review" | Any option with a human step |
| "without reducing capability" | Any option that removes tools/features |
| "entirely contained within one function/file" | Any option that expands scope (plan mode, explore) |
| "at the tool interface level" | Prompt-instruction answers |
| "fits within the context window" | File-path / reference answers |
| "built-in persistence not available" | `--resume` (that's a CLI-only feature) |

**Read constraints BEFORE evaluating options.** This is the single biggest time-saver and the trap you hit most.

### Step 3 — Eliminate, don't select
Cross out every option that:
- Violates a stated constraint (Step 2)
- Is the approach the question already said failed ("detailed instructions still produce inconsistent output" → more instructions is dead)
- Invents a fake feature (`CLAUDE_REVIEW_CRITERIA`, `--review-profile wcag`, "batch API doesn't support tool definitions")
- Makes an absolute claim that's technically false ("X cannot be done without Y")

### Step 4 — Mechanism check on survivors (THE step you skip)
For each remaining option, ask: **"Does this concrete change actually move the specific number from Step 1?"**

Not "is this in the right architectural family?" — but "does this specific intervention fix the specific mechanism?"

> This is exactly where I (Claude) got the tiered-findings question wrong. B (tiering) was the right *family* but didn't reduce per-finding investigation time. D (inline reasoning) eliminated the click-to-read cycle — the actual mechanism. **Family-match is not mechanism-match.**

---

## PART 2 — HOW TO PRIORITISE OPTIONS (the fix hierarchy)

When multiple options "work," prefer fixes higher up this ladder. Lower = weaker, more reactive.

```
STRONGEST ↑
1. Structural / schema-level   → makes the wrong outcome IMPOSSIBLE
   (split tools, validated schema, structured output contract,
    purpose-specific tool, frontmatter like allowed-tools / context:fork)

2. Architectural              → fix at the producer / source
   (mandatory metadata at ingestion, structured returns from subagents,
    intermediate clustering/normalisation agent, isolate noisy work in subagent)

3. Interception              → block before execution
   (PreToolCall hook validating args)

4. Detection / reactive      → catch after it happens
   (PostToolUse hook, downstream filter, blacklist, /compact, summariser agent)

5. Prompt-level              → suggest / discourage (model can ignore)
   (system prompt instruction, "be conservative", description text)
WEAKEST ↓
```

**The recurring trap:** I (you) keep reaching for level 4–5 (reactive/prompt) when the question wants level 1–2 (structural/architectural). When a question says "guarantee," "most robust," "most effective," "at the interface level," or "frequently violates" → go UP the ladder.

### The two mental models for this
- **"Don't label the wrong drawer — remove the drawer."** (schema vs description)
- **"Don't add a janitor when you can stop the mess at the source."** (fix at producer, not downstream)

---

## PART 3 — HOW TO STAY INSIDE THE SCOPE OF THE QUESTION

This is your biggest personal trap: **solving for production reality / multiple objectives when the question only asked for one.**

### The rule
> The exam wants the **minimum sufficient fix for the STATED problem**. It does not reward optimising for things the question didn't mention.

### Your specific failure modes
1. **Optimising for an unstated objective.** On the self-critique question you optimised for latency. Latency was never named as a constraint. → Only optimise for what the question states.
2. **Production over-engineering.** You picked file-paths for subagents, manual secret handling, dynamic decomposition — all defensible in production, none what the *question* asked. → Exam ≠ production. Answer the question on the page.
3. **Importing real-world API knowledge as a tiebreaker.** Sometimes correct (OpenAI allows consecutive user messages), but only relevant if the question is about that API. Anthropic's strict turn-alternation is the answer when the question is about Anthropic.

### The discipline
Before picking the "best-fit considering everything" option, ask:
- Did the question actually mention the thing I'm optimising for?
- Am I adding a concern (latency, cost, future-proofing) the question is silent on?

If yes → drop that concern and re-evaluate against only the stated problem.

### The exam-vs-production split (memorise this)
| Question signals... | Answer for... |
|---|---|
| "Multi-Agent Research System", "research report" | Separate synthesis agent (specialised) |
| Simple agentic coding, 1–2 subagents | Coordinator can synthesise itself (like Claude Code) |
| "fits within context window" | Pass by value (inline) |
| "500K tokens" / "too large" | Pass by reference (file path / retrieval) |
| Names a constraint you'd normally trade off | Honour the constraint absolutely; don't trade |

---

## PART 4 — THE PROMPT-ENGINEERING DECISION TREE (your most-tested area)

This is the "few-shot vs X" family you hit 5+ times. Lock the signal phrases.

| Problem signature | Right answer | Signal phrases |
|---|---|---|
| Learn a **consistent pattern / nuanced judgment** | **Few-shot examples** | "generalise its understanding", "contextual reasoning", prose requirements keep being misinterpreted |
| **Objective binary classification**, no nuance | **Explicit criteria in prompt** | clear rule exists, just needs stating |
| **Too many false positives / floods output** (filtering allowed) | **Explicit include + exclude criteria** | "flooded with", "buries the real issues", "only flag X" |
| Output quality **inconsistent in unpredictable, case-specific ways** | **Self-critique / evaluator-optimizer** | "varies by case", "different gaps each time", "inconsistent omissions" |
| Need consistent **classification across instances** | **Criteria + concrete examples per class** | "same issue rated differently", severity inconsistency |
| Must **avoid invalid outputs structurally** | **Schema enforcement, not prompt** | "frequently hallucinates parameters", "can ignore the rule" |

### Two specific clarifications you needed
- **Few-shot vs self-critique:** Few-shot teaches a *known* pattern you can demonstrate. Self-critique catches *unknown, variable* gaps you can't enumerate. If you can't list the failure cases (because they differ every time) → self-critique.
- **Few-shot vs more-precise-prose:** When detailed prose instructions ALREADY failed ("still produces inconsistent output"), more precise prose won't help — switch from *describing* to *demonstrating*. Examples eliminate interpretation because they aren't interpretations.

### The killer mental model
> **Few-shot teaches a known pattern. Self-critique catches unknown gaps. Schema makes the wrong output impossible. Prose only suggests.**

---

## PART 5 — EVALUATOR / CONFIDENCE / ROUTING (the calibration family)

### Evaluator-optimizer (self-critique) — when?
- A separate pass/model evaluates a draft before it's finalised.
- Use for **high-stakes quality** (legal translation, financial extraction) AND for **case-specific variable gaps**.
- Separate evaluator > inline self-flag because the generator has a conflict of interest grading its own work.
- Mental model: **"Would you trust a surgeon to grade their own surgery?"**

### Confidence score routing — when?
- Model self-reports confidence; route low-confidence items to humans.
- **Only valid when the model's underlying JUDGMENT is correct but UNCERTAIN.**
- **WRONG when the model's judgment itself is broken** (miscategorising) — a confidence score from broken judgment is still broken.
- Diagnostic: "uncertain about coverage of own output" → confidence routing. "miscategorises what's what" → fix judgment with criteria + few-shot.
- Mental model: **"Confidence routing trusts the judgment. Few-shot calibration fixes the judgment."**

### Tiering by severity — when?
- Use when you **cannot reduce volume** (constraint forbids filtering) but need to make a list manageable.
- All items stay visible; they're just prioritised (blocking vs suggestion).
- BUT: tiering reorganises — it doesn't reduce per-item cost. If the bottleneck is *per-item investigation time*, tiering alone may not be the fix (see inline-reasoning correction).
- Mental model: **"When you can't reduce the number of items, reduce cognitive load per item."**

### Escalation triggers — capability, not emotion
- Escalate on **case complexity / capability boundary**, NOT on sentiment/profanity/anger.
- Angry customer + simple problem = resolve with empathy. Calm customer + complex problem = escalate.
- For catastrophic + suspicious requests (data wipe, "SYSTEM OVERRIDE", prompt injection): **escalate IMMEDIATELY, no investigation, no MFA first.** Authentication ≠ authorisation ≠ "should this proceed at all."
- Mental models: **"Escalate on complexity, not temperature."** / **"A fire alarm doesn't check your ID before sounding."**

---

## PART 6 — MULTI-AGENT SYSTEMS (your weak scenario — drill this)

### What crosses agent boundaries
Each agent passes forward LESS than it holds. Raw material stays in the agent that processed it; only **distilled findings** travel.

```
Web/Doc subagent (isolated context):
  holds: raw pages / full document / reasoning chains
  passes: structured findings only {claim, source, relevance}
        ↓
Coordinator (router, NOT re-processor):
  holds: both subagents' returned findings + user question
  passes: those findings + question  (does NOT re-read raw material)
        ↓
Synthesizer (fresh, focused context):
  receives: question + web findings + doc findings (~distilled)
  produces: unified integrated output
```

### Key facts you were missing
- The coordinator **does not carry out research** — subagents do. Coordinator is a **conduit for findings**.
- Subagents have **isolated context** — they do NOT share session state with the coordinator or each other. (This is why "subagent can access the doc from session state" is a wrong assumption — pass it explicitly.)
- Synthesis is a **separate agent** in research systems because integration is its own specialised job; bundling it into the coordinator causes attention dilution. In *simple* systems (Claude Code-like), coordinator-synthesises is fine.

### Coordinator-as-hub advantages (pick the strategic, multi-benefit answer)
Observability + consistent error handling + context curation. Avoid options that overclaim a single tactical feature ("retries impossible without it" — false).

### Token bloat fix (Q30 lesson)
If subagent outputs are too big for the synthesizer: **change what upstream agents RETURN (structured findings)**, don't add a downstream summariser. Fix at the source.

### Tool distribution (Q26 lesson)
A document agent searching the web = wrong tool scope. Fix = **replace the general tool with a purpose-scoped one** (`load_document` validating document formats), not a prompt instruction saying "only use it for documents."

---

## PART 7 — CLAUDE CODE & TOOLING SPECIFICS

### Built-in tool selection
| Need | Tool |
|---|---|
| Find files by **name/pattern** | **Glob** (`**/V2.*.sql`) — does NOT respect `.gitignore` |
| Find **text inside files** | **Grep** — DOES skip `.gitignore` |
| Read file contents | Read |
| Edit a unique string | Edit (`old_str` must be **globally unique** — expand anchor until unique) |
| Overwrite whole file | Write |
| Structured data (JSON/XML) | `jq` / `xmlstarlet` — structure-aware, NOT `sed`/`grep`/`str_replace` |

- Mental model: **"Glob finds files by name. Grep finds lines inside them."**
- Mental model: **"Text tools see characters. Structure-aware tools see data."** (use jq when "not robust to formatting" / "could modify other data")
- Edit tool takes NO line numbers — pure string match.

### CLAUDE.md hierarchy
- Files **stack like CSS specificity** — they don't replace each other.
- Root `CLAUDE.md` = global standards. `services/payment/CLAUDE.md` = scoped override (loads on-demand when Claude works in that dir).
- `.claude/rules/` with `globs:` frontmatter = file-pattern-scoped rules (cross-cutting concerns).
- Locality problem → subdirectory `CLAUDE.md`. Pattern problem → `.claude/rules/` + globs.
- Version-controlled review criteria in CI/CD → put in repo's `CLAUDE.md` (NOT env vars, NOT machine-level config).

### Custom Slash Commands — frontmatter is the enforcement layer
| Frontmatter | Solves |
|---|---|
| `argument-hint` | Missing args (autocomplete prompt at invocation) |
| `context: fork` | Context bleeding (isolated subagent execution) |
| `allowed-tools` | Destructive/unwanted tool calls (whitelist) |
| `description` | Discoverability |
| `model` | Cost/quality routing |
- Mental model: **"Frontmatter is the schema layer. SKILL.md content is the prompt layer."** Three failures → three frontmatter features.

### Plan mode vs direct execution vs explore subagent
| Situation | Use |
|---|---|
| Scope fully known, single file/function, simple | **Direct execution** |
| Scope unclear, multi-file, architectural implications | **Plan mode** |
| Need to understand codebase first | **Explore subagent** |
| A phase produces verbose output that pollutes context | **Explore/subagent isolation** (BEFORE bloat, not `/compact` after) |
- Context management hierarchy: **1) prevent bloat (subagent) > 2) reference-not-content > 3) `/compact` (reactive) > 4) `--resume` new session.** You keep reaching for `/compact` (reactive) when subagent isolation (preventive) is available.

### Session state
- `--resume <name>` = **Claude Code CLI feature only**. Restores conversation history. Does NOT sync filesystem — tell Claude what changed after resuming.
- API is **stateless** — you are the memory layer. No built-in persistence → **structured summary, store, re-inject** (not `--resume`).
- Scratchpad / agentic memory: write discoveries to file/memory tool, **read before generating** (both halves required). Use for "agent forgot earlier discovery". Use `/compact`-style context editing for "context window full".
- State checkpointing (long-running): store **structured progress manifest** ("store the map, not the journey"), NOT full raw transcript replay. Chatbot-style "store all messages, replay" doesn't scale to multi-hour multi-agent work.

---

## PART 8 — TOOL DESIGN & API PARAMETERS

### Tool design
- Too many overlapping tools (19-tool monolith) → **split into specialised subagents, 4–5 tools each** (routing + specialisation). Not `tool_choice`.
- Polymorphic tool with generic params (`manage_aws_resource` + `action` + generic JSON) → **split into purpose-specific tools** with strict schemas. Makes invalid params impossible.
- Schema enforcement (optional fields + extraction instruction) beats forcing required fields (causes hallucination) or optional-only (causes omission).

### tool_choice
| Value | Guarantee |
|---|---|
| `{"type":"auto"}` | may call a tool or respond in text |
| `{"type":"any"}` | must call SOME tool |
| `{"type":"tool","name":"X"}` | must call tool X specifically |
- `disable_parallel_tool_use: true` → exactly one tool call.
- **Incompatible with extended thinking** (`any`/`tool` error with thinking).
- It's a **turn-level execution constraint** — controls IF a tool is called, NOT which gets selected accurately or argument quality. Don't use it to fix selection/hallucination problems (those are structural).

### Parameters that DON'T exist in Anthropic API
- `presence_penalty`, `frequency_penalty`, `logit_bias`, `logprobs`, `seed` — these are **OpenAI** params, silently ignored. Sampling params (`temperature`, `top_p`, `top_k`) shape token probability; they **cannot enforce output structure** (use few-shot/schema for format).

### Message Batches API
- `custom_id` = correlation key (results return out of order). Encode routing metadata here (`tenant|user|doc`). Must be unique per batch. **No PII** in it. Results are JSONL.
- **Batch CANNOT do iterative client-side tool loops** — each request runs to completion then stops; it can't pause for your code to execute a tool and resume. Server-side tools (web_search, code_execution) work in batch; **client-side tools requiring the agentic loop do not.** This is an architectural limit, not a latency one.

### Programmatic Tool Calling
- Model writes code to orchestrate loops/state (e.g. heterogeneous pagination across DBs).
- Use when the model **loses track of loop state across many calls** / context bloats from intermediate results. Move the loop OUT of reasoning INTO code. Not few-shot (that teaches *how*, doesn't fix state-tracking).

---

## PART 9 — PROVENANCE, SECURITY, SAFETY

### Information provenance / multi-source synthesis
- Temporal "contradictions" (same bill differs week to week) → **enforce `data_collection_timestamp` at ingestion**, build a timeline. Fix at write-time, not via synthesis-agent prompt.
- Estimate-vs-final discrepancies → **mandatory `report_type` + `report_date` metadata at ingestion**, not prompt tolerance rules.
- Redundant claims from 2 sources → **claim-clustering / entity-resolution agent** merges into one object with a `sources[]` array. Don't concatenate (inflates apparent evidence, loses provenance mapping).
- Mental model: **"Provenance = enforce at write time. You can't instruct your way to provenance."**

### Security / escalation / injection
- Catastrophic + suspicious ("SYSTEM OVERRIDE", data wipe, fund transfer with fake auth) → **escalate immediately + flag injection + STOP.** Don't validate, don't run MFA, don't just error-reject.
- Firewall-style cross-arg rules ("IP can't be in both lists", "0.0.0.0/0 needs override flag") → **PreToolCall hook validating args before execution.** "Pre" = nothing has executed yet. Backend "upon receipt" validation = too late (data already arrived). System prompt = unreliable. PostToolUse = damage done.
- Mental model: **"PreToolCall = bouncer at the door. Backend validation = security inside the venue (too late)."**

---

## PART 10 — THE TRAPS I KEPT FALLING INTO (read this last, before the exam)

1. **Reactive over preventive.** Reached for `/compact`, downstream summariser, blacklist filter when subagent-isolation / structured-source-output / whitelist was the real fix. → Go UP the fix ladder.
2. **Prompt over structural.** Picked "update the description" / "add an instruction" when schema / hook / separate-tool enforces it. → "Guarantee/most robust/interface-level" = structural.
3. **Optimising for unstated objectives.** Added latency/cost/production concerns the question never mentioned. → Only optimise for stated constraints.
4. **Family-match instead of mechanism-match.** Picked the right *category* of answer that didn't actually move the specific number. → Run the Step-4 mechanism check.
5. **Confidence/conservative language.** "Be conservative", "high-confidence", "use judgment" are almost always wrong. → Named criteria beat adjectives.
6. **Environment confusion.** Mixed up Claude Code (`--resume`, CLI) vs API (stateless) vs MCP. → Identify the environment from signal words first.
7. **Missing pre-disqualifying constraints.** Didn't read "stakeholders rejected filtering" before evaluating. → Constraints first, options second.
8. **Trusting a confident wrong explanation** (mine, on the tiering question). → If your mechanism check conflicts with an authority's confident claim, trust the mechanism check.

---

## QUICK PRE-EXAM CHECKLIST (the 30-second version)

1. What's the **exact broken mechanism**? (not the topic)
2. What **constraints** silently kill options?
3. Cross out: constraint-violators, already-failed approaches, fake features, absolute-claim overstatements.
4. For survivors: **does this specifically move the number?** (mechanism check)
5. Prefer **structural > architectural > interception > reactive > prompt.**
6. Am I optimising for something the question **didn't mention**? Stop if yes.
7. Which **environment** (API / Claude Code / MCP)?
