import os
import pytest
from frio_intel.agents_internal.internal_analyst import DATA_DIR, FILES

def test_data_files_exist():
    for f in FILES:
        assert (DATA_DIR / f).exists(), f"missing {f}"

@pytest.mark.skipif(not os.environ.get("OPENAI_API_KEY") and not os.environ.get("MODEL"),
                    reason="needs LLM env")
def test_crew_builds():
    from frio_intel.agents_internal.internal_analyst import _build
    crew = _build()
    assert len(crew.agents) == 1 and len(crew.tasks) == 1
