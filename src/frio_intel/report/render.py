from datetime import date
from pathlib import Path
import markdown as md_lib
from .models import ExecutiveBrief

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
{brief.executive_summary}

## The Question & Why Now
{brief.question_and_why_now}

## Market Landscape
{brief.market_landscape}

## Competitive Dynamics
{brief.competitive_dynamics}

## Frio's Position
{brief.frio_position}

## Strategic Options
{_options_table(brief)}

## Recommendation & Next Steps
{brief.recommendation_and_next_steps}

### Risks & Open Questions
{brief.risks_and_open_questions}

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
