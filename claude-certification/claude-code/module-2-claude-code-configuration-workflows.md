# Module 2: Claude Code Configuration & Workflows

This module is about separating repository rules, user rules, and session state so the system remains predictable. The main failure mode here is mixing policy, memory, and runtime control into one undifferentiated pile.

## Anti-patterns to avoid

- no `CLAUDE.md`: leaves the repo with no durable operating rules.
- flat rules: everything has the same priority, so nothing has a clear scope.
- prompt-only repository standards: standards vanish as soon as the prompt changes.
- wrong scope for repo rules: project policy leaks into user policy or vice versa.
- mixing CLI state with API state: creates confusion about what is durable and what is session-local.
- `--resume` confusion: resuming a session is not the same as reconstructing config state.
- relying on `/compact` first: compaction is a pressure valve, not a design strategy.
- ignoring settings precedence: produces contradictory behavior that is hard to debug.
- using user rules for project rules: the wrong layer now has to carry repo-specific intent.

## Pattern tradeoffs

- `CLAUDE.md` hierarchy: gives a clear inheritance model, but only if people respect scope.
- `CLAUDE.local.md`: useful for local overrides without polluting shared policy.
- user-level rules: good for personal defaults, but dangerous as a substitute for repo rules.
- project rules: keep repo behavior stable across contributors.
- managed policy: valuable for centrally enforced constraints, especially in shared environments.
- settings precedence: makes conflicts debuggable when the hierarchy is explicit.
- permission modes: let you tune safety versus convenience.
- plan mode: useful for thinking before acting, but not a replacement for execution discipline.
- session management: helps preserve continuity without pretending memory is free.
- `/memory`: good for durable working memory when used sparingly.
- prompt caching: improves efficiency, but it can also hide stale assumptions.
- `claudeMdExcludes`: prevents unwanted instruction inheritance in nested trees.
- skills for reusable behavior: great for standardization and reuse.
- YAML frontmatter: useful for metadata, but only if you keep it consistent.
- directory-qualified skill names: help disambiguate behavior in larger repos.
- nested skills: allow local specialization, at the cost of more policy surface.
- GitHub Actions workflows: make automation reproducible and reviewable.

## Topic notes

### Claude Code overview
**Pros:** Helps you reason about where config lives, how sessions behave, and which layer owns which decision.
**Cons:** People often use the overview as a substitute for actually mapping their own repo rules.

### How Claude Code works
**Pros:** Knowing the operational model makes configuration choices less arbitrary.
**Cons:** The mechanics are easy to overgeneralize into rules that do not fit a specific repo.

### `.claude` directory
**Pros:** A clear home for project-local state, memory, and support files.
**Cons:** If you dump too much into it, the directory becomes an unstructured attic.

### store instructions and memories
**Pros:** Separates durable guidance from ephemeral chat context.
**Cons:** If everything becomes "memory," nothing is actually authoritative.

### manage sessions
**Pros:** Keeps long-running work coherent and reduces accidental context loss.
**Cons:** Session continuity can hide stale assumptions if you do not refresh intent explicitly.

### common workflows
**Pros:** Good for making repeated work predictable and reviewable.
**Cons:** Workflows that are too rigid do not survive variation well.

### prompt library
**Pros:** Reuse saves time and improves consistency.
**Cons:** Libraries rot fast if they are not curated against real usage.

### best practices
**Pros:** Encode what has already been learned to work in the repo.
**Cons:** "Best practice" without a concrete scope becomes vague advice.

### settings
**Pros:** Central point for behavior control.
**Cons:** Too many settings produce hidden coupling and hard-to-debug precedence issues.

### managed settings
**Pros:** Strong governance for shared environments.
**Cons:** Can feel restrictive when local experimentation is needed.

### permission settings
**Pros:** Control the blast radius of risky operations.
**Cons:** Excessively strict permissions make simple workflows annoying.

### project settings
**Pros:** Keep behavior tied to the project instead of the person.
**Cons:** They need maintenance as the project changes.

### user settings
**Pros:** Good for personal defaults and comfort.
**Cons:** A bad place to encode repo policy.

### global settings
**Pros:** Reduce repeated setup across projects.
**Cons:** Global defaults can quietly override local intent if you are not careful.

### skill files
**Pros:** Package behavior into reusable, named units.
**Cons:** If overused, they become another layer of indirection.

### `SKILL.md`
**Pros:** A durable contract for behavior and invocation.
**Cons:** If the file is too broad, it stops being a useful contract.

### `allowed-tools`
**Pros:** Restricts what a skill can use, which improves safety and clarity.
**Cons:** Too narrow and the skill becomes unusable.

### `disable-model-invocation`
**Pros:** Useful when a skill should only expose static behavior or deterministic steps.
**Cons:** Removes flexibility when the task really does need model reasoning.

### `description`
**Pros:** Gives fast routing signal and helps selection.
**Cons:** Weak descriptions produce weak tool or skill choice.

### `name`
**Pros:** Stable identifier for reuse and composition.
**Cons:** Poor naming creates ambiguity across nested scopes.

### `context: fork`
**Pros:** Lets you branch work cleanly without contaminating the parent context.
**Cons:** Forks increase the number of states you have to reconcile later.

### slash-command skills
**Pros:** Fast access for common behaviors and workflows.
**Cons:** They can become a second hidden API if documented poorly.

### nested skill variants
**Pros:** Support specialization by directory or scope.
**Cons:** More variants means more chance of accidental mismatch.

### code review automation
**Pros:** Makes review repeatable and can catch obvious regressions early.
**Cons:** Automated review is only as good as the policy and context it receives.

### CI/CD integration
**Pros:** Pushes validation closer to the change, which reduces surprises later.
**Cons:** CI that mirrors bad local assumptions just automates the wrong thing faster.

## Exam pattern

### What the question is usually testing

- Whether you know which layer owns repo rules, user rules, global settings, and runtime session state.
- Whether you can distinguish durable project configuration from ephemeral CLI state.
- Whether you can tell when a question is about Claude Code behavior versus API behavior.
- Whether you choose the right mechanism for reuse: `CLAUDE.md`, skills, hooks, or workflows.

### What to notice first

- Words like `project`, `user`, `global`, `settings precedence`, `resume`, `session`, `memory`, `skills`, `hooks`, `plan mode`, or `CLAUDE.md`.
- Phrases about "team-wide", "repo-wide", "personal", or "local override".
- Mentions of enforcement, automation, or repeatability.
- Any statement about instructions needing to persist across sessions or across contributors.

### How to eliminate wrong answers

- Eliminate answers that put project policy in user-level settings.
- Eliminate answers that rely on prompt-only standards when the issue is durable repo behavior.
- Eliminate answers that use `/compact` as the primary design strategy.
- Eliminate answers that confuse `--resume` with persistence or synchronization.

### How to answer correctly

- Put repo policy in `CLAUDE.md` and local overrides in `CLAUDE.local.md` when needed.
- Use user settings only for personal defaults, not shared standards.
- Use skills for reusable behaviors and hooks for enforcement or automation.
- Treat `.claude` as the project-local support area and respect settings precedence when there is overlap.
- If the question is about operational discipline, prefer the layer that makes the behavior durable and visible.

### Common question shapes

- "Where should this instruction live?" -> choose the narrowest durable scope that matches the audience.
- "What survives between sessions?" -> memory, files, and settings; not raw chat state.
- "What is the right place for repo standards?" -> `CLAUDE.md`, not user settings.
- "How do you enforce a recurring action?" -> hooks or workflows, not prompt reminders.

### Short answer rule

- If it is shared repo policy, put it in repo-scoped config.
- If it is personal preference, keep it in user settings.
- If it is execution-time enforcement, use hooks or automation.
- If it is just a transient task, keep it in the session.
