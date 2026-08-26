"""Synthesis crew: defined in code (not config) because it carries the
deterministic report contract (output_pydantic=ExecutiveBrief)."""
from crewai import Agent, Task, Crew, Process
from frio_intel.report.models import ExecutiveBrief

def _build() -> Crew:
    writer = Agent(
        role="Executive Strategy Writer",
        goal=("Merge external market research and Frio's internal findings into a decisive, "
              "cited executive brief answering: {question}"),
        backstory=("You write for a Fortune 500 executive team: verdict first, evidence after, "
                   "no hedging filler. You weave internal and external evidence together and keep "
                   "numbered citations [n] tied to the source list. You never invent facts beyond "
                   "the findings given to you."),
        verbose=True,
    )
    task = Task(
        description=(
            "Question: {question}\n\n"
            "EXTERNAL FINDINGS (public web, each fact has a URL):\n{external_findings}\n\n"
            "INTERNAL FINDINGS (Frio internal files, each fact has a filename):\n{internal_findings}\n\n"
            "Populate every field of the ExecutiveBrief schema. Rules:\n"
            "- executive_summary: verdict in the first sentence, then exactly 3 bullets "
            "(market signal / internal signal / timing & risk).\n"
            "- Build the sources list FIRST, before writing any other section. Every DISTINCT URL "
            "from EXTERNAL FINDINGS gets exactly ONE source number, no matter how many facts from it "
            "you use or how many sections cite it - never create more than one source entry for the "
            "same URL. Every Frio internal file you actually use as evidence (e.g. "
            "sales_by_category.csv, brand_portfolio.json, strategy_memo_2025.md) MUST appear as its "
            "own separate source entry, with kind='internal' and locator set to that exact filename - "
            "an internal fact is not fully cited until its file has its own numbered entry.\n"
            "- Only after the sources list is final, cite inline as [n] throughout all sections. Every "
            "[n] you write MUST resolve to the source list entry for the exact document that fact came "
            "from: never point an internal fact's citation at a web source's number, never point a web "
            "fact's citation at an internal source's number, and never reuse one source's number for a "
            "different source.\n"
            "- strategic_options: exactly Build, Acquire, Partner; mark exactly one recommended=True.\n"
            "- question_and_why_now MUST reference what the 2025 internal memo decided and what changed.\n"
            "- frio_position uses ONLY internal findings; market sections use ONLY external findings.\n"
            "- risks_and_open_questions: state what the evidence does NOT settle."
        ),
        expected_output="A fully populated ExecutiveBrief object.",
        output_pydantic=ExecutiveBrief,
        agent=writer,
    )
    return Crew(agents=[writer], tasks=[task], process=Process.sequential, verbose=True)

def run_synthesis(question: str, external: str, internal: str) -> ExecutiveBrief:
    result = _build().kickoff(inputs={
        "question": question, "external_findings": external, "internal_findings": internal,
    })
    if result.pydantic is None:
        raise RuntimeError("Synthesis did not produce a valid ExecutiveBrief")
    return result.pydantic
