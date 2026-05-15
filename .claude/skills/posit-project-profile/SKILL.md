---
name: posit-project-profile
description: Project purpose, aesthetic, and success criteria for this Posit evaluation harness. Use whenever generating Plotnine or Great Tables code, judging outputs, rewriting skills, or documenting the repo so Codex and Claude Code preserve the user's intended style and evaluation philosophy.
---

# Posit Project Profile

This project is an evaluation harness for LLM-generated Posit-style Python workflows. Its purpose is not only to get one chart or table right, but to build reusable agent skills that improve through measurable feedback.

## User Purpose

The user is building a portfolio-quality, agent-facing evaluation system for Plotnine charts and Great Tables workflows.

The system should demonstrate:

- grammar-of-graphics reasoning rather than prompt guessing,
- executable generated code rather than prose-only answers,
- concrete eval checks and judge reasoning,
- reusable skill files that Codex and Claude Code can both load,
- a self-improving loop where failed evals update skill guidance.

## Aesthetic

Prefer a style that is:

- compact and instructional,
- Posit-flavored and grammar-of-graphics aware,
- code-first, with examples that run,
- explicit about data, aesthetics, geoms, stats, facets, labels, themes, and output saving,
- polished enough for a technical portfolio, but not marketing-heavy.

Avoid:

- vague "best practices" prose,
- generic visualization advice without Plotnine syntax,
- decorative or over-styled chart instructions that distract from eval requirements,
- long tutorials when a small reusable example would teach the pattern.

## Agent Behavior

When acting as Codex or Claude Code inside this repo:

1. Start from `posit-repository` for routing.
2. For Plotnine work, traverse `plotnine-grammar-of-graphics` graph nodes.
3. Use the project profile as a constraint on generated code, judge rubrics, skill rewrites, and documentation.
4. Prefer changes that make future agent behavior more reliable, not just the current answer nicer.
5. Keep eval prompts, graph nodes, generated-code expectations, and grader checks aligned.

## Optimization Goal

The best output is one that:

- satisfies the user prompt,
- runs locally,
- produces a nonblank visual/table artifact,
- follows the active grammar graph,
- uses concise reusable patterns,
- improves future Codex and Claude Code behavior.

When optimizing skill files, preserve this profile. Skill rewrites should make nodes more useful for the user's purpose: compact examples, graph-aware reasoning, and measurable eval improvement.

## Few-Shot Style Examples

### Good Plotnine Guidance

```text
For a grouped scatter plot, map numeric variables to x/y and use `color='factor(cyl)'` when cylinder count is categorical. Pair `geom_point()` with `geom_smooth(method='lm', se=False)` only when the prompt asks for a trend line.
```

### Good Eval-Facing Skill Rewrite

```text
Add a small `after_stat(...)` example to `layer-stat-computed-labels.md` when bar-label evals fail `uses_after_stat` or `uses_format_string`.
```

### Good Reporting Voice

```text
The harness prompts a model for Plotnine code, executes the generated script, checks graph-aligned requirements, judges the rendered chart, and writes a report that explains what failed.
```
