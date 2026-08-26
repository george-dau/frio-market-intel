import re
from datetime import date
from pathlib import Path
import markdown as md_lib
from .models import ExecutiveBrief

_LIST_ITEM_RE = re.compile(r"^\s*([-*]\s+|\d+\.\s+)")

def _normalize_lists(text: str) -> str:
    """Insert a blank line before a list block that immediately follows
    prose. Python's `markdown` lib (unlike GitHub's CommonMark) requires a
    blank line before a list, so agent-written text like
    "Lead sentence.\\n- bullet" would otherwise collapse into one <p> with
    literal dashes instead of a real <ul>."""
    lines = text.split("\n")
    out: list[str] = []
    for line in lines:
        if out:
            prev = out[-1]
            if _LIST_ITEM_RE.match(line) and prev.strip() != "" and not _LIST_ITEM_RE.match(prev):
                out.append("")
        out.append(line)
    return "\n".join(out)

def _options_table(brief: ExecutiveBrief) -> str:
    head = "| Option | Speed | Cost | Risk | Fit with Frio assets | |\n|---|---|---|---|---|---|"
    rows = [
        f"| {o.name} | {o.speed} | {o.cost} | {o.risk} | {o.asset_fit} | "
        f"{'**Recommended**' if o.recommended else ''} |"
        for o in brief.strategic_options
    ]
    return "\n".join([head, *rows])

def _sources(brief: ExecutiveBrief) -> str:
    lines = []
    for s in brief.sources:
        loc = f"[{s.locator}]({s.locator})" if s.kind == "web" else f"`{s.locator}` (internal)"
        lines.append(f"{s.id}. {s.title} - {loc}")
    return "\n".join(lines)

def render_markdown(brief: ExecutiveBrief) -> str:
    return f"""# Frio Market Intelligence Brief: {brief.title}

**Question:** {brief.question}
**Prepared:** {date.today().isoformat()} | **Prepared by:** Frio Market Intelligence (CrewAI)

## Executive Summary
{_normalize_lists(brief.executive_summary)}

## The Question & Why Now
{_normalize_lists(brief.question_and_why_now)}

## Market Landscape
{_normalize_lists(brief.market_landscape)}

## Competitive Dynamics
{_normalize_lists(brief.competitive_dynamics)}

## Frio's Position
{_normalize_lists(brief.frio_position)}

## Strategic Options
{_options_table(brief)}

## Recommendation & Next Steps
{_normalize_lists(brief.recommendation_and_next_steps)}

### Risks & Open Questions
{_normalize_lists(brief.risks_and_open_questions)}

## Sources
{_sources(brief)}
"""

_HTML_SHELL = (Path(__file__).parent / "template.html").read_text

def render_html(brief: ExecutiveBrief) -> str:
    body = md_lib.markdown(render_markdown(brief), extensions=["tables"])
    return _HTML_SHELL().replace("{{TITLE}}", brief.title).replace("{{BODY}}", body)

def save_report(brief: ExecutiveBrief, out_dir: Path, slug: str) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{slug}.md"
    html_path = out_dir / f"{slug}.html"
    md_path.write_text(render_markdown(brief))
    html_path.write_text(render_html(brief))
    return md_path, html_path
