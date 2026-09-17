# Dify DSL Subagent Review Overview

[ภาษาไทย](dify-dsl-subagent-review-overview.th.md) · [简体中文](dify-dsl-subagent-review-overview.zh-CN.md) · [Documentation index](README.md)

This page answers four questions:

1. When should `dify-dsl-subagent-review` be used?
2. How does it differ from `review / governance / authoring / refactor`?
3. What review modes does it support?
4. Which repository cases already validate those modes?

## Positioning

`dify-dsl-subagent-review` is not a new primary business skill. It is a **review orchestration skill**.

It is responsible for:

- organizing multi-review read-only checks
- deciding between parallel, serial, single-subagent, or no-subagent fallback
- merging review-side and governance-side conclusions when needed

It is not responsible for:

- first-hop routing
- generating DSL from scratch
- directly modifying DSL
- replacing the core judgment of `authoring / review / refactor / governance`

## One-Screen Path

<!-- BEGIN ROUTE_MATRIX -->
| User goal | Recommended entry | Common next step |
| --- | --- | --- |
| Requirements still unclear | `using-dify-dsl` or `dify-dsl-brainstorming` | `dify-dsl-authoring / review / refactor` |
| Create a new DSL | `using-dify-dsl` or `dify-dsl-authoring` | Use `dify-dsl-subagent-review` when complexity or risk is high |
| Review an existing DSL read-only | `using-dify-dsl` or `dify-dsl-review` | Escalate to `dify-dsl-subagent-review` for formal multi-review |
| Modify an existing DSL | `using-dify-dsl` or `dify-dsl-refactor` | Use `dify-dsl-subagent-review` after risky changes |
| Only choose a template | `using-dify-dsl` or `dify-dsl-templates` | Move to `dify-dsl-authoring` if a full draft is needed |
| Only decide whether it is deliverable | `using-dify-dsl` or `dify-dsl-governance` | Use `dify-dsl-subagent-review` first only when the user explicitly wants multi-review or conflict merge |
| Explicitly organize multi-review | `using-dify-dsl` or `dify-dsl-subagent-review` | Pick parallel / serial / single-subagent / no-subagent fallback |
<!-- END ROUTE_MATRIX -->

The main path is:

<!-- BEGIN MAIN_PATH -->
```text
using-dify-dsl
-> brainstorming / authoring / review / refactor / templates / governance / subagent-review
-> use subagent-review or governance again only when needed
```
<!-- END MAIN_PATH -->

## When To Use

Use it when:

- you already have a DSL draft or an existing DSL
- the user explicitly asks for multi-review or independent reviewers
- you want field, graph, prompt, and gate judgments separated
- you expect review-side and governance-side conclusions to diverge
- you need a stable fallback path when subagents are unavailable

Do not use it when:

- requirements are still unclear
- you have not yet chosen `authoring / review / refactor`
- a normal single-thread review is enough
- the user only wants direct refactoring

## Relationship To Other Skills

- `using-dify-dsl`
  Handles top-level routing. If the user explicitly asks for multi-review orchestration, it routes here.
- `dify-dsl-authoring`
  Produces the draft first. High-risk drafts can then flow here for structured review.
- `dify-dsl-review`
  Good for ordinary read-only review. Escalate here when formal multi-review is needed.
- `dify-dsl-refactor`
  Applies changes first. If the changed DSL needs independent review, route here next.
- `dify-dsl-governance`
  Produces gate and delivery conclusions. If the user explicitly wants multi-review or conflict merge, this orchestrator should run first.

## Four Review Modes

### 1. Asynchronous Parallel

Use when:

- multiple risk surfaces exist at once
- the sample is moderately or highly complex
- you want fast, independent opinions first

Default roles:

- field-constraint reviewer
- graph-closure reviewer
- prompt-and-contract reviewer

Optional:

- release-readiness reviewer

### 2. Synchronous Serial

Use when:

- later judgment depends on earlier structural confirmation
- the next stage only makes sense if the previous stage holds
- the sample is small but strongly staged

Typical order:

1. structure / fields
2. prompt and I/O contracts
3. gate merge if needed

### 3. Single Subagent

Use when:

- the risk surface is narrow
- the main issue belongs to one role
- adding more reviewers would mostly duplicate the same conclusion

Typical sample:

- `broken-selector.yml`

### 4. No Subagent

Use only when:

- the platform does not support subagents
- the current session policy forbids them
- the user explicitly disallows them

In that case, the workflow must:

- run a complete self-check
- explicitly say `independent review not performed`
- upgrade the result to at least `needs manual confirmation`

## Current Role Set

- field-constraint reviewer
- graph-closure reviewer
- prompt-and-contract reviewer
- release-readiness reviewer

The first three gather raw opinions. The last one only appears when gate merging or conflict arbitration is actually needed.

## Platform setup and limits

The files in `skills/dify-dsl-quality/agents/` are role instructions. This repository's installer exposes skills; it does not install these roles as named custom agents in `.claude/agents/`. In Claude Code, pass the role instructions and relevant file paths to an available subagent, or separately configure a custom agent with read-only tool access. See [Claude Code subagent documentation](https://code.claude.com/docs/en/sub-agents).

In Claude.ai and Codex, inspect the actual tools and session permissions before delegating. Installing or uploading a skill does not establish independent-agent availability. If unavailable, use the no-subagent fallback and report that independent review was not performed. See the [Claude setup guide](../.claude/INSTALL.th.md) and [platform overview](README.md).

New app output targets DSL `0.7.0`; RAG Pipeline retains `0.1.0`. Historical fixtures are regression evidence, not current output templates. Agent App and portable Agent v2 packages remain outside this pack's validated generation scope. See the [version policy and primary sources](../skills/dify-dsl-foundations/references/dsl-version-policy.th.md).

Platform sources checked via Exa on 2026-09-17.

## Current Coverage

These are stored cases and replay assertions. `validate_forward_testing.py` checks case structure, lint, and saved outputs; it does not launch fresh model sessions or independent reviewers. Live Claude Code, Claude.ai, and Dify import/runtime tests require separate evidence. A passing lint result alone does not establish Dify compatibility.

### Ideal paths

- `orchestrate-readonly-review`
- `merge-release-readiness`

### Fallback path

- `degrade-no-subagent`

### Conflict merge

- `merge-rag-review-vs-governance`
- `merge-chat-review-vs-governance`

### Mode selection

- `select-serial-chat-review`
- `select-single-graph-review`

### Upstream integration

- `route-to-subagent-review`
- `route-full-lifecycle-rag`
- `knowledge-retrieval-authoring-needs-review`
- `refactor-retrieval-topk-needs-review`

## Suggested Reading Order

For a first read:

1. [using-dify-dsl](../skills/using-dify-dsl/SKILL.md)
2. [dify-dsl-subagent-review](../skills/dify-dsl-subagent-review/SKILL.md)
3. [mode-selection-matrix](../skills/dify-dsl-subagent-review/references/mode-selection-matrix.md)
4. [orchestration-playbook](../skills/dify-dsl-subagent-review/references/orchestration-playbook.md)
5. [subagent-review](../skills/dify-dsl-quality/references/subagent-review.md)

## Current Status

At this point, the subagent review layer is no longer just a design idea. It now has:

- a dedicated skill
- a mode decision matrix
- an orchestration playbook
- fallback rules
- conflict merge paths
- upstream integration points
- stored-case and replay regression coverage; live platform behavior remains a separate verification step
