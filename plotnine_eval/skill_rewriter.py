"""
DSPy-optimized skill rewriting for the Plotnine grammar graph.

This tool makes skill rewriting agentic through DSPy itself:

1. `compile` builds a DSPy trainset from failed eval cases and optimizes a
   graph-node rewrite module with MIPROv2.
2. `propose` runs the compiled rewriter to produce scoped Markdown node
   replacement proposals.
3. `apply` writes a reviewed proposal back to the graph node files.

The optimizer is self-supervised by eval patterns: failed checks imply target
nodes, rewrite constraints, and quality criteria. The metric rewards scoped,
valid, check-addressing node rewrites rather than broad prose churn.

Usage:
    python plotnine_eval/skill_rewriter.py compile --report plotnine_eval_report.json
    python plotnine_eval/skill_rewriter.py propose --report plotnine_eval_report.json
    python plotnine_eval/skill_rewriter.py apply --proposal plotnine_skill_rewrite_proposals.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import dspy

try:
    from .project_profile import load_project_profile
except ImportError:
    from project_profile import load_project_profile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAPH_ROOT = PROJECT_ROOT / ".claude" / "skills" / "plotnine-grammar-of-graphics"
GRAPH_PATH = GRAPH_ROOT / "graph" / "graph.json"
DEFAULT_REPORT = PROJECT_ROOT / "plotnine_eval_report.json"
FALLBACK_REPORT = PROJECT_ROOT / "plotnine_eval" / "plotnine_eval_report.json"
DEFAULT_PROPOSAL_PATH = PROJECT_ROOT / "plotnine_skill_rewrite_proposals.json"
DEFAULT_COMPILED_PATH = Path(__file__).resolve().parent / "compiled_skill_rewriter.json"
DEFAULT_MODEL = os.getenv("PLOTNINE_SKILL_REWRITER_MODEL", "anthropic/claude-sonnet-4-5")


CHECK_NODE_HINTS = {
    "executes_without_error": ["concept-ggplot-object"],
    "uses_geom_point": ["primitive-point"],
    "uses_geom_bar": ["primitive-bar"],
    "uses_geom_histogram": ["primitive-histogram"],
    "uses_geom_boxplot": ["primitive-boxplot"],
    "uses_geom_jitter": ["primitive-jitter"],
    "uses_geom_line": ["primitive-line"],
    "uses_geom_smooth": ["primitive-smooth"],
    "uses_geom_text": ["primitive-text"],
    "uses_after_stat": ["layer-stat-computed-labels", "primitive-text"],
    "uses_format_string": ["layer-stat-computed-labels", "primitive-text"],
    "cyl_as_factor": ["layer-aesthetic-mapping"],
    "uses_factor": ["layer-aesthetic-mapping"],
    "uses_fill": ["layer-aesthetic-mapping"],
    "uses_color_fill": ["layer-aesthetic-mapping"],
    "uses_facet": ["layer-facets"],
    "uses_facet_wrap": ["layer-facets"],
    "uses_labs": ["layer-labels-theme"],
    "has_axis_labels": ["layer-labels-theme"],
    "uses_theme_minimal": ["layer-labels-theme"],
    "uses_theme_bw": ["layer-labels-theme"],
    "uses_theme_classic": ["layer-labels-theme"],
    "uses_theme_light": ["layer-labels-theme"],
    "uses_theme_override": ["layer-labels-theme"],
    "hides_legend": ["layer-labels-theme"],
    "uses_element_text": ["layer-labels-theme"],
    "saves_plot": ["output-save"],
    "image_nonblank": ["output-save", "grader-plotnine-eval"],
    "llm_judge": ["grader-plotnine-eval"],
    "vision_judge": ["grader-plotnine-eval"],
}


CHECK_TERMS = {
    "uses_after_stat": ["after_stat"],
    "uses_format_string": ["format_string"],
    "cyl_as_factor": ["factor("],
    "uses_factor": ["factor("],
    "uses_facet": ["facet_"],
    "uses_facet_wrap": ["facet_wrap"],
    "saves_plot": ["save", "output.png"],
    "uses_labs": ["labs"],
    "has_axis_labels": ["labs", "x=", "y="],
    "uses_theme_minimal": ["theme_minimal"],
    "uses_theme_bw": ["theme_bw"],
    "uses_theme_classic": ["theme_classic"],
    "uses_theme_light": ["theme_light"],
    "uses_theme_override": ["theme("],
    "hides_legend": ["legend_position"],
    "uses_element_text": ["element_text"],
    "uses_geom_point": ["geom_point"],
    "uses_geom_bar": ["geom_bar"],
    "uses_geom_histogram": ["geom_histogram"],
    "uses_geom_boxplot": ["geom_boxplot"],
    "uses_geom_jitter": ["geom_jitter"],
    "uses_geom_line": ["geom_line"],
    "uses_geom_smooth": ["geom_smooth"],
    "uses_geom_text": ["geom_text"],
}

PROFILE_TERMS = [
    "grammar",
    "plotnine",
    "example",
    "eval",
    "graph",
    "code",
    "save",
]


SELF_SUPERVISION_POLICY = """
Optimize persistent Plotnine graph-node skill text from failed eval patterns.

Self-supervision rules:
- Failed checks imply which graph nodes need better guidance or examples.
- A good rewrite is scoped to implicated node IDs and does not touch unrelated nodes.
- A good rewrite preserves the node heading, graph identity, and Markdown shape.
- A good rewrite adds concrete Plotnine examples that would have prevented the failed checks.
- A good rewrite aligns prompt intent, grammar node, generated-code expectation, and grader evidence.
- A good rewrite preserves the project profile: compact, instructional, Posit-flavored, graph-aware, code-first, and evaluation-driven.
- Avoid broad style advice. Prefer small code patterns, counterexamples, and eval-facing reminders.

Return JSON only:
{
  "summary": "what failure pattern the rewrite addresses",
  "updates": [
    {
      "node_id": "layer-stat-computed-labels",
      "reason": "why this node should change",
      "new_text": "complete replacement Markdown for the node"
    }
  ]
}
"""


@dataclass
class Node:
    id: str
    type: str
    path: Path
    text: str


def load_graph() -> dict[str, Any]:
    with open(GRAPH_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_nodes() -> dict[str, Node]:
    graph = load_graph()
    nodes: dict[str, Node] = {}
    for node in graph["nodes"]:
        path = GRAPH_ROOT / node["file"]
        if path.exists():
            nodes[node["id"]] = Node(node["id"], node["type"], path, path.read_text(encoding="utf-8"))
    return nodes


def load_report(path: Path) -> dict[str, Any]:
    if not path.exists() and path == DEFAULT_REPORT and FALLBACK_REPORT.exists():
        path = FALLBACK_REPORT
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def failed_cases(report: dict[str, Any], case_id: str | None = None) -> list[dict[str, Any]]:
    cases = [case for case in report.get("cases", []) if case.get("tool", "plotnine") == "plotnine"]
    selected = [case for case in cases if not case.get("passed")]
    if case_id:
        selected = [case for case in selected if case.get("id") == case_id]
    return selected


def failed_check_names(case: dict[str, Any]) -> list[str]:
    return [check["name"] for check in case.get("checks", []) if not check.get("passed", False)]


def implicated_nodes(case: dict[str, Any], nodes: dict[str, Node]) -> list[str]:
    active = [node for node in case.get("graph_nodes", []) if node in nodes]
    implicated: list[str] = []
    for check_name in failed_check_names(case):
        implicated.extend(CHECK_NODE_HINTS.get(check_name, []))
    if not implicated:
        implicated.extend(active)

    allowed = set(active) or set(nodes)
    seen: set[str] = set()
    result = []
    for node_id in implicated:
        if node_id in nodes and node_id in allowed and node_id not in seen:
            result.append(node_id)
            seen.add(node_id)

    for fallback in ("layer-aesthetic-mapping", "layer-labels-theme", "grader-plotnine-eval"):
        if fallback in allowed and fallback in nodes and fallback not in seen:
            result.append(fallback)
            seen.add(fallback)
    return result[:6]


def compact_case(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": case.get("id"),
        "category": case.get("category"),
        "prompt": case.get("prompt"),
        "score": case.get("score"),
        "failed_checks": [check for check in case.get("checks", []) if not check.get("passed", False)],
        "graph_nodes": case.get("graph_nodes", []),
        "llm_judge": case.get("llm_judge"),
        "vision_judge": case.get("vision_judge"),
        "generated_code": case.get("generated_code", "")[:3500],
    }


def node_payload(nodes: dict[str, Node]) -> dict[str, dict[str, str]]:
    return {
        node_id: {
            "type": node.type,
            "relative_path": str(node.path.relative_to(PROJECT_ROOT)),
            "current_text": node.text,
        }
        for node_id, node in nodes.items()
    }


def json_from_text(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    raw = match.group(0) if match else text
    return json.loads(raw)


def configure_dspy_lm(dspy, model: str) -> None:
    if dspy.settings.lm:
        return
    if os.getenv("ANTHROPIC_API_KEY"):
        dspy.configure(lm=dspy.LM(model, api_key=os.getenv("ANTHROPIC_API_KEY")))
        return
    if os.getenv("GEMINI_API_KEY"):
        dspy.configure(lm=dspy.LM(os.getenv("PLOTNINE_SKILL_REWRITER_GEMINI_MODEL", "gemini/gemini-2.5-pro"), api_key=os.getenv("GEMINI_API_KEY")))
        return
    raise RuntimeError("Set ANTHROPIC_API_KEY or GEMINI_API_KEY before running DSPy skill rewriting.")


def mipro_v2_optimizer(dspy, metric, num_trials: int):
    optimizer_cls = getattr(dspy, "MIPROv2", None)
    if optimizer_cls is None:
        from dspy.teleprompt import MIPROv2

        optimizer_cls = MIPROv2
    return optimizer_cls(metric=metric, auto="light", num_trials=num_trials)


def make_rewriter_program_class(dspy):
    class RewriteSkillNodes(dspy.Signature):
        """Rewrite Plotnine graph-node Markdown so future generations avoid observed eval failures."""

        failure_context: str = dspy.InputField(desc="JSON describing failed checks, prompt, graph path, judge feedback, and generated code.")
        candidate_nodes: str = dspy.InputField(desc="JSON mapping candidate node IDs to current node Markdown.")
        project_profile: str = dspy.InputField(desc="User/project purpose, aesthetic, and optimization criteria.")
        rewrite_policy: str = dspy.InputField(desc="Self-supervised rewrite policy and output schema.")
        proposal_json: str = dspy.OutputField(desc="Valid JSON with summary and scoped node updates only.")

    class SkillRewriteProgram(dspy.Module):
        def __init__(self):
            self.rewrite = dspy.ChainOfThought(RewriteSkillNodes)

        def forward(self, failure_context: str, candidate_nodes: str, project_profile: str, rewrite_policy: str):
            return self.rewrite(
                failure_context=failure_context,
                candidate_nodes=candidate_nodes,
                project_profile=project_profile,
                rewrite_policy=rewrite_policy,
            )

    return SkillRewriteProgram


def build_case_example(dspy, case: dict[str, Any], all_nodes: dict[str, Node]):
    candidates = {node_id: all_nodes[node_id] for node_id in implicated_nodes(case, all_nodes)}
    failed_checks = failed_check_names(case)
    return dspy.Example(
        failure_context=json.dumps(compact_case(case), indent=2),
        candidate_nodes=json.dumps(node_payload(candidates), indent=2),
        project_profile=load_project_profile(),
        rewrite_policy=SELF_SUPERVISION_POLICY,
        expected_node_ids=json.dumps(list(candidates)),
        failed_checks=json.dumps(failed_checks),
        case_id=case.get("id", ""),
    ).with_inputs("failure_context", "candidate_nodes", "project_profile", "rewrite_policy")


def build_trainset(dspy, cases: list[dict[str, Any]], all_nodes: dict[str, Node]) -> list:
    return [build_case_example(dspy, case, all_nodes) for case in cases]


def proposal_metric(example, prediction, trace=None) -> float:
    try:
        proposal = json_from_text(getattr(prediction, "proposal_json", ""))
    except Exception:
        return 0.0

    expected_nodes = set(json.loads(example.expected_node_ids))
    failed_checks = json.loads(example.failed_checks)
    updates = proposal.get("updates", [])
    if not isinstance(updates, list) or not updates:
        return 0.05

    score = 0.2
    updated_nodes = [update.get("node_id") for update in updates]
    valid_scope = [node_id for node_id in updated_nodes if node_id in expected_nodes]
    score += 0.2 * (len(valid_scope) / max(1, len(updated_nodes)))
    score += 0.15 * min(1.0, len(set(valid_scope)) / max(1, min(3, len(expected_nodes))))

    markdown_ok = 0
    concise_ok = 0
    term_hits = 0
    profile_hits = 0
    needed_terms = [term for check in failed_checks for term in CHECK_TERMS.get(check, [])]
    needed_terms_lower = [term.lower() for term in needed_terms]

    for update in updates:
        text = str(update.get("new_text", ""))
        if text.strip().startswith("# ") and "## Examples" in text:
            markdown_ok += 1
        if 80 <= len(text) <= 4000:
            concise_ok += 1
        lower = text.lower()
        if any(term in lower for term in needed_terms_lower):
            term_hits += 1
        if any(term in lower for term in PROFILE_TERMS):
            profile_hits += 1

    score += 0.15 * (markdown_ok / len(updates))
    score += 0.1 * (concise_ok / len(updates))
    if needed_terms_lower:
        score += 0.15 * min(1.0, term_hits / max(1, min(len(updates), len(needed_terms_lower))))
    else:
        score += 0.1
    score += 0.05 * (profile_hits / len(updates))

    summary = str(proposal.get("summary", ""))
    reasons = " ".join(str(update.get("reason", "")) for update in updates)
    if any(check in summary or check in reasons for check in failed_checks):
        score += 0.05

    return min(score, 1.0)


def select_failed_cases(report_path: Path, case_id: str | None, max_cases: int) -> list[dict[str, Any]]:
    report = load_report(report_path)
    cases = failed_cases(report, case_id)[:max_cases]
    if not cases:
        raise SystemExit("No failed Plotnine cases found for skill rewriting.")
    return cases


def compile_rewriter(args) -> None:
    configure_dspy_lm(dspy, args.model)
    all_nodes = load_nodes()
    cases = select_failed_cases(args.report, args.case_id, args.max_cases)
    trainset = build_trainset(dspy, cases, all_nodes)
    SkillRewriteProgram = make_rewriter_program_class(dspy)
    optimizer = mipro_v2_optimizer(dspy, proposal_metric, args.trials)
    compiled = optimizer.compile(SkillRewriteProgram(), trainset=trainset)
    compiled.save(str(args.compiled_out))
    print(f"Saved compiled DSPy skill rewriter -> {args.compiled_out}")


def validate_updates(proposal: dict[str, Any], candidate_nodes: dict[str, Node]) -> dict[str, Any]:
    valid_updates = []
    for update in proposal.get("updates", []):
        node_id = update.get("node_id")
        new_text = update.get("new_text", "")
        if node_id not in candidate_nodes:
            continue
        if not isinstance(new_text, str) or not new_text.strip().startswith("# "):
            continue
        valid_updates.append(
            {
                "node_id": node_id,
                "path": str(candidate_nodes[node_id].path.relative_to(PROJECT_ROOT)),
                "reason": update.get("reason", ""),
                "new_text": new_text.rstrip() + "\n",
            }
        )
    return {"summary": proposal.get("summary", ""), "updates": valid_updates}


def write_proposal(path: Path, proposal: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(proposal, f, indent=2)


def propose_rewrites(args) -> None:
    configure_dspy_lm(dspy, args.model)
    all_nodes = load_nodes()
    cases = select_failed_cases(args.report, args.case_id, args.max_cases)
    candidate_ids: list[str] = []
    for case in cases:
        candidate_ids.extend(implicated_nodes(case, all_nodes))
    candidates = {node_id: all_nodes[node_id] for node_id in dict.fromkeys(candidate_ids)}

    SkillRewriteProgram = make_rewriter_program_class(dspy)
    program = SkillRewriteProgram()
    if args.compiled.exists() and not args.no_load:
        program.load(str(args.compiled))

    failure_context = json.dumps([compact_case(case) for case in cases], indent=2)
    candidate_context = json.dumps(node_payload(candidates), indent=2)
    prediction = program(
        failure_context=failure_context,
        candidate_nodes=candidate_context,
        project_profile=load_project_profile(),
        rewrite_policy=SELF_SUPERVISION_POLICY,
    )
    raw_proposal = json_from_text(prediction.proposal_json)
    proposal = validate_updates(raw_proposal, candidates)
    proposal.update(
        {
            "source_report": str(args.report),
            "case_ids": [case.get("id") for case in cases],
            "compiled_rewriter": str(args.compiled) if args.compiled.exists() and not args.no_load else None,
            "model": args.model,
            "project_profile": "posit-project-profile",
        }
    )
    write_proposal(args.proposal_out, proposal)
    print(f"Saved {len(proposal['updates'])} proposed skill node update(s) -> {args.proposal_out}")


def apply_updates(proposal: dict[str, Any], nodes: dict[str, Node]) -> None:
    for update in proposal.get("updates", []):
        node_id = update["node_id"]
        if node_id not in nodes:
            raise RuntimeError(f"Unknown node in proposal: {node_id}")
        node = nodes[node_id]
        resolved = node.path.resolve()
        if not resolved.is_relative_to(GRAPH_ROOT.resolve()):
            raise RuntimeError(f"Refusing to write outside graph root: {resolved}")
        resolved.write_text(update["new_text"], encoding="utf-8")


def apply_proposal(args) -> None:
    nodes = load_nodes()
    proposal = load_report(args.proposal)
    apply_updates(proposal, nodes)
    print(f"Applied {len(proposal.get('updates', []))} skill node update(s) from {args.proposal}")


def main() -> None:
    parser = argparse.ArgumentParser(description="DSPy-optimize and apply Plotnine skill graph rewrites.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser("compile", help="Optimize the skill rewriter with DSPy MIPROv2.")
    compile_parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    compile_parser.add_argument("--case-id", default=None)
    compile_parser.add_argument("--max-cases", type=int, default=6)
    compile_parser.add_argument("--trials", type=int, default=5)
    compile_parser.add_argument("--model", default=DEFAULT_MODEL)
    compile_parser.add_argument("--compiled-out", type=Path, default=DEFAULT_COMPILED_PATH)
    compile_parser.set_defaults(func=compile_rewriter)

    propose_parser = subparsers.add_parser("propose", help="Generate rewrite proposals using the compiled rewriter.")
    propose_parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    propose_parser.add_argument("--case-id", default=None)
    propose_parser.add_argument("--max-cases", type=int, default=3)
    propose_parser.add_argument("--model", default=DEFAULT_MODEL)
    propose_parser.add_argument("--compiled", type=Path, default=DEFAULT_COMPILED_PATH)
    propose_parser.add_argument("--proposal-out", type=Path, default=DEFAULT_PROPOSAL_PATH)
    propose_parser.add_argument("--no-load", action="store_true")
    propose_parser.set_defaults(func=propose_rewrites)

    apply_parser = subparsers.add_parser("apply", help="Apply a reviewed proposal JSON to graph node files.")
    apply_parser.add_argument("--proposal", type=Path, default=DEFAULT_PROPOSAL_PATH)
    apply_parser.set_defaults(func=apply_proposal)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
