# Claude Code Study Game Plan

## 1. Module 1: Agentic Architecture & Orchestration

### Anti-patterns

- `stop_reason` ignored
- text parsing instead of `stop_reason`
- monolithic agent
- wrong orchestration shape
- missing error propagation
- shared context between subagents
- vague tool boundaries
- synthesis inside the wrong agent

### Patterns

- branch on `stop_reason`
- loop back on `tool_use`
- return `tool_result`
- specialized agents
- hub-and-spoke
- sequential pipelines
- task decomposition
- structured findings
- orchestrator-worker
- evaluator-optimizer
- routing
- parallelization
- fallback paths

### Topic names

- Claude turn lifecycle
- Messages API turn flow
- `tool_use` blocks
- `tool_result` blocks
- `end_turn`
- `max_tokens`
- client tools
- server tools
- tool search tool
- large-context tool selection
- interleaved thinking
- extended thinking
- agentic loop
- multi-agent orchestration
- subagent context isolation
- context passing
- lifecycle hooks
- error propagation
- retry logic
- escalation logic

## 2. Module 2: Claude Code Configuration & Workflows

### Anti-patterns

- no `CLAUDE.md`
- flat rules
- prompt-only repository standards
- wrong scope for repo rules
- mixing CLI state with API state
- `--resume` confusion
- relying on `/compact` first
- ignoring settings precedence
- using user rules for project rules

### Patterns

- `CLAUDE.md` hierarchy
- `CLAUDE.local.md`
- user-level rules
- project rules
- managed policy
- settings precedence
- permission modes
- plan mode
- session management
- `/memory`
- prompt caching
- `claudeMdExcludes`
- skills for reusable behavior
- YAML frontmatter
- directory-qualified skill names
- nested skills
- GitHub Actions workflows

### Topic names

- Claude Code overview
- How Claude Code works
- `.claude` directory
- store instructions and memories
- manage sessions
- common workflows
- prompt library
- best practices
- settings
- managed settings
- permission settings
- project settings
- user settings
- global settings
- skill files
- `SKILL.md`
- `allowed-tools`
- `disable-model-invocation`
- `description`
- `name`
- `context: fork`
- slash-command skills
- nested skill variants
- code review automation
- CI/CD integration

## 3. Module 3: Prompt Engineering & Structured Output

### Anti-patterns

- contradictory instructions
- more prose after prose already failed
- no examples
- no schema for structure
- no validation loop
- confidence as correctness
- irrelevant context
- overfitting to one wording

### Patterns

- few-shot prompting
- explicit criteria
- JSON schema
- XML structuring
- role prompting
- thinking
- prompt chaining
- prompt generator
- templates and variables
- prompt improver
- structured outputs
- prefill
- validation-retry
- self-critique
- evaluator-optimizer
- extraction patterns
- context engineering

### Topic names

- Prompting best practices
- clarity
- examples
- XML structuring
- role prompting
- thinking
- prompt chaining
- structured outputs
- JSON
- XML
- custom templates
- response prefill
- output consistency
- few-shot examples
- explicit criteria prompts
- consistency guardrails
- validation-retry loops
- self-review passes

## 4. Module 4: Tool Design & MCP

### Anti-patterns

- mega-tools
- vague tool descriptions
- stateful tools without retry safety
- too many tools at once
- prompt instructions used as interface enforcement
- treating resources like tools
- missing access controls
- missing rate limits
- unsanitized outputs

### Patterns

- one tool, one responsibility
- precise descriptions
- input schema
- output schema
- annotations
- structured error responses
- user confirmation
- timeouts
- logging
- rate limiting
- output sanitization
- tool discovery
- pagination
- server-side tools
- client-side tools

### Topic names

- MCP specification
- MCP architecture
- MCP host
- MCP client
- MCP server
- initialization
- capabilities
- tools
- resources
- prompts
- `resources/list`
- `prompts/list`
- tool definitions
- `name`
- `title`
- `description`
- `inputSchema`
- `outputSchema`
- `annotations`
- MCP Inspector
- reference server implementations
- server quickstart
- client quickstart

## 5. Module 5: Context Management & Reliability

### Anti-patterns

- key info in the middle
- unstructured context growth
- no rolling summary
- sending everything everywhere
- one context track for every branch
- no human escalation
- confidence as a substitute for judgment
- ignoring rate-limit signals
- ignoring timeout errors

### Patterns

- progressive summarization
- rolling summary
- parallel extraction
- `context: fork`
- external memory
- state persistence
- fallback strategies
- human-in-the-loop escalation
- confidence calibration
- circuit breaker
- prompt caching
- tool context management

### Topic names

- context windows
- 200k context
- large input documents
- lost-in-the-middle
- prompt caching
- interleaved thinking
- extended thinking
- tool context management
- rate limits
- `retry-after`
- `429`
- `504`
- `529`
- `request_too_large`
- `permission_error`
- error handling
- long-context behavior
- external memory

## 6. Cross-module topics

### Anti-patterns

- fixing the wrong mechanism
- optimizing for unstated goals
- choosing prompt tweaks for structural problems
- confusing Claude Code CLI behavior with API behavior
- confusing tools, resources, and prompts
- using reactive cleanup when preventive isolation exists
- treating confidence as correctness

### Patterns

- read constraints first
- eliminate by mechanism
- choose structural fixes first
- keep the minimum sufficient fix
- preserve provenance at ingestion
- validate before execution when stakes are high
- isolate risky work
- summarize before context overload

### Topic names

- Messages API
- tool use
- structured outputs
- errors
- rate limits
- batch processing
- provenance
- prompt injection
- pre-execution validation
- evaluator-optimizer
- progressive summarization
- rolling summaries
- parallel extraction
- `context: fork`
