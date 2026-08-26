from pathlib import Path

from crewai.project import load_crew

_CREW_FILE = Path(__file__).with_name("crew.jsonc")


def _build():
    crew, default_inputs = load_crew(_CREW_FILE)
    return crew, default_inputs


def run_external_research(question: str) -> str:
    crew, defaults = _build()
    result = crew.kickoff(inputs={**defaults, "question": question})
    return result.raw


async def run_external_research_async(question: str) -> str:
    crew, defaults = _build()
    result = await crew.kickoff_async(inputs={**defaults, "question": question})
    return result.raw
