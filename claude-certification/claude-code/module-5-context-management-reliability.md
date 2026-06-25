# Module 5: Context Management & Reliability

This module is about keeping the right information available without letting context become a landfill. Reliability work here is mostly about choosing what to retain, what to summarize, and when to escalate.

## Anti-patterns to avoid

- key info in the middle: important facts get lost when they are buried in long context.
- unstructured context growth: makes retrieval, summarization, and auditability worse over time.
- no rolling summary: forces every turn to re-read everything.
- sending everything everywhere: creates token waste and confusion.
- one context track for every branch: leads to duplication and divergent state.
- no human escalation: the system keeps grinding on cases it should hand off.
- confidence as a substitute for judgment: fluent output is not a reliability strategy.
- ignoring rate-limit signals: guarantees avoidable failures.
- ignoring timeout errors: leaves you blind to infrastructure and service problems.

## Pattern tradeoffs

- progressive summarization: keeps long-running work usable, but summaries can lose detail.
- rolling summary: good for preserving state, though it needs careful upkeep.
- parallel extraction: efficient for fact gathering, but merge quality matters.
- `context: fork`: clean way to branch work while preserving the parent state.
- external memory: moves durable state out of the live context window.
- state persistence: useful for continuity across sessions.
- fallback strategies: improve survivability when a primary path fails.
- human-in-the-loop escalation: essential for ambiguity, risk, or repeated failure.
- confidence calibration: helps the system know when to trust itself less.
- circuit breaker: prevents repeated failure loops from wasting time.
- prompt caching: cuts cost and latency on repeated context.
- tool context management: keeps tool state scoped and relevant.

## Topic notes

### context windows
**Pros:** Set the hard envelope for what can be considered at once.
**Cons:** The limit is real, so large windows can encourage sloppy packing.

### 200k context
**Pros:** Lets you keep more source material live without constant compression.
**Cons:** Large windows do not eliminate lost-signal problems, and they can still be expensive.

### large input documents
**Pros:** Useful when you need the model to work from primary source material directly.
**Cons:** Long docs often need chunking, extraction, or summarization to be reliable.

### lost-in-the-middle
**Pros:** Naming the problem helps you design around it instead of pretending position does not matter.
**Cons:** There is no magic fix; you still need ordering, summaries, and extraction.

### prompt caching
**Pros:** Reduces repeated work and improves responsiveness.
**Cons:** Cached context can encourage stale assumptions if you do not refresh it carefully.

### interleaved thinking
**Pros:** Useful when the model has to alternate between observing, deciding, and acting.
**Cons:** The more interleaving you do, the more you need explicit state boundaries.

### extended thinking
**Pros:** Helpful for complex reasoning or planning.
**Cons:** It can hide poor context management if you lean on it for every hard case.

### tool context management
**Pros:** Keeps tool inputs and outputs scoped so the model is not swimming in irrelevant state.
**Cons:** Requires discipline in what you pass forward and what you discard.

### rate limits
**Pros:** Protect service stability and help enforce fairness.
**Cons:** They can disrupt workflows unless you design retries and backoff around them.

### `retry-after`
**Pros:** Gives a direct signal for when a retry is reasonable.
**Cons:** Not every client respects it, which defeats the point.

### `429`
**Pros:** Clear signal that the caller is exceeding allowed throughput.
**Cons:** It is easy to treat as a transient nuisance when it is really a capacity or policy issue.

### `504`
**Pros:** Indicates a timeout at the gateway or upstream boundary.
**Cons:** If you retry blindly, you may just repeat a slow failure path.

### `529`
**Pros:** Communicates overloaded service conditions explicitly.
**Cons:** Needs proper backoff or the system will amplify pressure.

### `request_too_large`
**Pros:** Prevents oversized payloads from wasting compute.
**Cons:** Requires the client to chunk, trim, or summarize intentionally.

### `permission_error`
**Pros:** Stops unauthorized or unsafe operations early.
**Cons:** If permissions are poorly understood, legitimate work fails noisily.

### error handling
**Pros:** The backbone of robust systems; it decides what happens when things fail.
**Cons:** Error handling that is too generic can hide the true problem.

### long-context behavior
**Pros:** Lets you reason about how the system degrades as input size grows.
**Cons:** Long-context capability can tempt you into skipping structure and relevance control.

### external memory
**Pros:** Good for durable facts, preferences, and intermediate state that should outlive a turn.
**Cons:** External memory needs governance or it becomes stale, noisy, or unsafe.

## Exam pattern

### What the question is usually testing

- Whether you can see that the problem is context growth, not model intelligence.
- Whether you know when to summarize, fork, cache, or persist state externally.
- Whether you can recognize rate-limit and timeout handling as reliability mechanisms, not just error messages.
- Whether you understand that long-context capability does not remove the need for relevance control.

### What to notice first

- Words like `context window`, `lost in the middle`, `rolling summary`, `progressive summarization`, `fork`, `cache`, `429`, `504`, `529`, `retry-after`, `large document`, `persistent state`, or `external memory`.
- Phrases like "too much information", "long session", "re-read everything", or "keep continuity".
- Signs that the model needs to remember state without carrying every raw detail forward.

### How to eliminate wrong answers

- Eliminate answers that add more context instead of reducing or structuring it.
- Eliminate answers that rely only on prompt wording when the issue is state management.
- Eliminate retries without backoff when the question mentions rate limits or overload.
- Eliminate reactive cleanup if a preventative summary, fork, or external memory layer would solve the problem earlier.

### How to answer correctly

- Use progressive or rolling summaries when the session is long and the important state must survive.
- Use external memory or checkpointing when the state must persist beyond the live context window.
- Use `context: fork` or other branch isolation when multiple work streams would otherwise interfere.
- Respect rate-limit signals and choose backoff, circuit breaking, or retry-after handling.
- If the question is about robustness, answer with the mechanism that keeps the right information available without bloating the live context.

### Common question shapes

- "The session is too long and the model forgets earlier details." -> summarize or externalize state.
- "A long document is getting lost in the middle." -> structure, chunk, or extract.
- "The service is rate limiting." -> backoff and retry-after handling.
- "Multiple branches are interfering." -> fork and isolate context.

### Short answer rule

- If the bottleneck is state size, compress or externalize.
- If the bottleneck is overload, back off.
- If the bottleneck is branch interference, isolate.
- If the bottleneck is durability, persist.
