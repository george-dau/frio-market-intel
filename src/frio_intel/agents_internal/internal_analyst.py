"""Internal branch: a single agent (not a crew - bounded file analysis
doesn't need one). Reads Frio's mocked internal data with file tools."""
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
FILES = ["sales_by_category.csv", "brand_portfolio.json", "strategy_memo_2025.md"]

def _build() -> Crew:
    analyst = Agent(
        role="Internal Insights Analyst, Frio Beverage Company",
        goal=("Mine Frio's internal data for evidence relevant to: {question}. "
              "Report portfolio performance by category, launchable assets, and prior internal decisions."),
        backstory=("You are Frio's own analytics lead. You only state what the internal files support, "
                   "and you cite the source filename for every figure. You never use outside knowledge."),
        tools=[FileReadTool()],
        verbose=True,
    )
    file_list = "\n".join(f"- {DATA_DIR / f}" for f in FILES)
    task = Task(
        description=(
            "Read ALL of these Frio internal files:\n" + file_list + "\n\n"
            "Then answer, strictly from the files, for the question: {question}\n"
            "1) Which categories are growing vs flat (with figures and margins)?\n"
            "2) Which brands and distribution assets are relevant to the question?\n"
            "3) What did the 2025 strategy memo decide, and which of its open questions matter now?\n"
            "Cite the filename for every figure, e.g. [sales_by_category.csv]."
        ),
        expected_output=("Markdown with three sections: 'Portfolio performance', 'Launchable assets', "
                         "'Internal history (2025 memo)'; every figure cites its source filename."),
        agent=analyst,
    )
    return Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=True)

def run_internal_insights(question: str) -> str:
    return _build().kickoff(inputs={"question": question}).raw

async def run_internal_insights_async(question: str) -> str:
    return (await _build().kickoff_async(inputs={"question": question})).raw
