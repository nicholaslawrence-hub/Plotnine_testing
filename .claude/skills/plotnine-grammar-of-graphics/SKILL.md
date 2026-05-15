---
name: plotnine-grammar-of-graphics
description: Build, debug, or evaluate Plotnine charts through a grammar-of-graphics hierarchy. Use when working with ggplot objects, aes mappings, geometric primitives such as points/bars/lines/histograms/boxplots/text/smooths, stats, scales, facets, themes, or Plotnine eval graders in this repository.
---

# Plotnine Grammar Of Graphics

Use this as the Plotnine system skill. It is a small knowledge graph, not a flat checklist. Traverse from the user intent to grammar concepts, graphical primitives, aesthetic/stat layers, presentation layers, and eval grader checks.

## Graph Files

```text
plotnine-grammar-of-graphics/
+-- SKILL.md
+-- graph/
|   +-- graph.json
|   +-- traversal.md
|   +-- nodes/
|       +-- intent-*.md
|       +-- concept-*.md
|       +-- primitive-*.md
|       +-- layer-*.md
|       +-- output-*.md
|       +-- grader-*.md
|       +-- example-*.md
+-- assets/
    +-- fewshots/
        +-- *.png
+-- references/
    +-- older narrative references
```

## How To Traverse

1. Start with `graph/traversal.md`.
2. Load `graph/graph.json` when you need explicit node IDs and edge types.
3. Pick one or more `intent-*` nodes.
4. Follow `requires`, `uses`, `maps_to`, `pairs_with`, `exemplified_by`, and `graded_by` edges.
5. Load only the node files on the active path.

When generating code, prefer loading the matching `example-*` node as the few-shot. Those nodes include code and point to rendered PNG assets in `assets/fewshots/`.

## DSPy Skill Rewriting

Use `plotnine_eval/skill_rewriter.py` when eval failures should feed back into the graph node files. The script defines a DSPy `SkillRewriteProgram`, compiles it with `MIPROv2` over failed eval cases, and scores proposals with a self-supervised metric based on failed checks, implicated nodes, required Plotnine terms, Markdown validity, and scope control.

This workflow requires `dspy-ai`; the rewriter imports DSPy directly and should fail fast when DSPy is unavailable.

Compile the rewriter:

```bash
python plotnine_eval/skill_rewriter.py compile --report plotnine_eval_report.json --trials 5
```

Generate reviewable proposals:

```bash
python plotnine_eval/skill_rewriter.py propose --report plotnine_eval_report.json
```

Apply only after reviewing `plotnine_skill_rewrite_proposals.json`:

```bash
python plotnine_eval/skill_rewriter.py apply --proposal plotnine_skill_rewrite_proposals.json
```

This is the agentic self-supervision loop: eval failures define the optimization signal, DSPy optimizes the rewriter, and reviewed proposals update the persistent skill graph that Codex and Claude Code load.

Example traversal for a scatter plot with trend line:

```text
intent-relationship
-> concept-ggplot-object
-> layer-aesthetic-mapping
-> primitive-point
-> primitive-smooth
-> layer-labels-theme
-> output-save
-> grader-plotnine-eval
```

Example traversal for a bar chart with percent labels:

```text
intent-counts
-> concept-ggplot-object
-> layer-aesthetic-mapping
-> primitive-bar
-> layer-stat-computed-labels
-> primitive-text
-> layer-labels-theme
-> output-save
-> grader-plotnine-eval
```

## Core Rules

Use `from plotnine import *` in generated code unless the user explicitly asks for a different import style.

Quote dataframe columns inside `aes()`: `aes(x='mpg', y='hp')`.

Use `factor(...)` inside `aes()` when a numeric column should behave categorically: `aes(fill='factor(cyl)')`.

Use `after_stat(...)` and `format_string` for stat-computed labels instead of f-strings.

Assign the plot to `p` and save it with `p.save('output.png', ...)` in scripts and eval cases.
