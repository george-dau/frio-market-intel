#!/usr/bin/env python
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai.flow.flow import Flow, and_, listen, start

from frio_intel.agents_internal.internal_analyst import run_internal_insights_async
from frio_intel.crews.external_research.external_research import run_external_research_async
from frio_intel.crews.synthesis.synthesis import run_synthesis
from frio_intel.report.models import ExecutiveBrief
from frio_intel.report.render import save_report

load_dotenv()
REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"
DEFAULT_QUESTION = "Should Frio Beverage Company enter the functional beverage category?"

class BriefState(BaseModel):
    question: str = DEFAULT_QUESTION
    external_findings: str = ""
    internal_findings: str = ""
    brief: ExecutiveBrief | None = None
    report_paths: list[str] = []

class MarketBriefFlow(Flow[BriefState]):
    @start()
    def intake(self, crewai_trigger_payload: dict | None = None):
        if crewai_trigger_payload and crewai_trigger_payload.get("question"):
            self.state.question = crewai_trigger_payload["question"]
        return self.state.question

    @listen(intake)
    async def external_branch(self):
        self.state.external_findings = await run_external_research_async(self.state.question)

    @listen(intake)
    async def internal_branch(self):
        self.state.internal_findings = await run_internal_insights_async(self.state.question)

    @listen(and_(external_branch, internal_branch))
    def synthesize(self):
        self.state.brief = run_synthesis(
            self.state.question, self.state.external_findings, self.state.internal_findings
        )

    @listen(synthesize)
    def render_report(self):
        slug = "frio-brief-" + "".join(c if c.isalnum() else "-" for c in self.state.question.lower())[:60].strip("-")
        md_path, html_path = save_report(self.state.brief, REPORTS_DIR, slug)
        self.state.report_paths = [str(md_path), str(html_path)]
        return {"report_markdown": str(md_path), "report_html": str(html_path)}

def kickoff():
    flow = MarketBriefFlow()
    result = flow.kickoff()
    print("Reports written:", flow.state.report_paths)
    return result

def plot():
    MarketBriefFlow().plot()

if __name__ == "__main__":
    kickoff()
