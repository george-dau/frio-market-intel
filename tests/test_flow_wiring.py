import frio_intel.main as m
from frio_intel.report.models import ExecutiveBrief, Source, StrategicOption

def minimal_brief():
    return ExecutiveBrief(
        title="T", question="Q", executive_summary="E [1]", question_and_why_now="W",
        market_landscape="M", competitive_dynamics="C", frio_position="F",
        strategic_options=[StrategicOption(name="Acquire", speed="fast", cost="high",
                                           risk="med", asset_fit="fit", recommended=True)],
        recommendation_and_next_steps="R", risks_and_open_questions="K",
        sources=[Source(id=1, title="S", locator="https://example.com", kind="web")],
    )

def test_flow_runs_branches_and_renders(monkeypatch, tmp_path):
    calls = []
    async def fake_external(q): calls.append("external"); return "EXT[1]"
    async def fake_internal(q): calls.append("internal"); return "INT[2]"
    def fake_synth(q, e, i):
        assert e == "EXT[1]" and i == "INT[2]"
        calls.append("synth"); return minimal_brief()
    monkeypatch.setattr(m, "run_external_research_async", fake_external)
    monkeypatch.setattr(m, "run_internal_insights_async", fake_internal)
    monkeypatch.setattr(m, "run_synthesis", fake_synth)
    monkeypatch.setattr(m, "REPORTS_DIR", tmp_path)

    flow = m.MarketBriefFlow()
    flow.kickoff()
    assert calls.count("external") == 1 and calls.count("internal") == 1
    assert calls.index("synth") > calls.index("external") and calls.index("synth") > calls.index("internal")
    assert len(flow.state.report_paths) == 2
