from pathlib import Path
from frio_intel.report.models import ExecutiveBrief, Source, StrategicOption
from frio_intel.report.render import render_markdown, render_html, save_report

def fixture_brief():
    return ExecutiveBrief(
        title="Functional Beverage Category Entry",
        question="Should we enter the functional beverage category?",
        executive_summary="Enter via partner-then-acquire. [1]",
        question_and_why_now="Raised and tabled in 2025. [2]",
        market_landscape="Category grew fast. [1]",
        competitive_dynamics="Incumbents are buying, not building. [1]",
        frio_position="Core flat; Volt Focus pilot +40% YoY. [3]",
        strategic_options=[
            StrategicOption(name="Build", speed="slow", cost="med", risk="high", asset_fit="uses Volt brand"),
            StrategicOption(name="Acquire", speed="fast", cost="high", risk="med", asset_fit="instant shelf", recommended=True),
        ],
        recommendation_and_next_steps="Acquire within 12 months.",
        risks_and_open_questions="Valuations are elevated.",
        sources=[
            Source(id=1, title="Beverage Digest", locator="https://example.com/a", kind="web"),
            Source(id=2, title="2025 strategy memo", locator="strategy_memo_2025.md", kind="internal"),
            Source(id=3, title="Sales by category", locator="sales_by_category.csv", kind="internal"),
        ],
    )

def test_markdown_has_all_sections_in_order():
    md = render_markdown(fixture_brief())
    sections = ["Executive Summary", "The Question & Why Now", "Market Landscape",
                "Competitive Dynamics", "Frio's Position", "Strategic Options",
                "Recommendation & Next Steps", "Risks & Open Questions", "Sources"]
    idxs = [md.index(s) for s in sections]  # raises if missing
    assert idxs == sorted(idxs)

def test_markdown_options_table_marks_recommendation():
    md = render_markdown(fixture_brief())
    assert "| Acquire" in md
    assert "**Recommended**" in md

def test_html_renders_and_brands():
    html = render_html(fixture_brief())
    assert "Frio Beverage Company" in html and "<h2" in html
    assert "https://example.com/a" in html  # web citations are links

def test_save_report_writes_both(tmp_path):
    md_path, html_path = save_report(fixture_brief(), tmp_path, "test-run")
    assert md_path.exists() and html_path.exists()
    assert md_path.suffix == ".md" and html_path.suffix == ".html"

def test_list_immediately_after_prose_renders_as_real_list():
    brief = fixture_brief().model_copy(update={
        "executive_summary": "Verdict.\n- b1\n- b2",
    })
    md = render_markdown(brief)
    assert "Verdict.\n\n- b1" in md  # blank line inserted before the list
    html = render_html(brief)
    assert "<ul>" in html
    assert "<li>b1" in html
