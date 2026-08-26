import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY") and not os.environ.get("MODEL"),
    reason="crew construction requires an LLM configured in env",
)


def test_crew_builds():
    from frio_intel.crews.external_research.external_research import _build

    crew, _ = _build()
    assert len(crew.agents) == 2 and len(crew.tasks) == 2
