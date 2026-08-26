from pydantic import BaseModel, Field

class Source(BaseModel):
    id: int = Field(description="Citation number used inline as [n]")
    title: str
    locator: str = Field(description="URL for web sources; filename for internal sources")
    kind: str = Field(description="'web' or 'internal'")

class StrategicOption(BaseModel):
    name: str = Field(description="e.g. 'Build', 'Acquire', 'Partner'")
    speed: str
    cost: str
    risk: str
    asset_fit: str = Field(description="How it fits Frio's existing brands/distribution")
    recommended: bool = False

class ExecutiveBrief(BaseModel):
    """The Frio Market Intelligence Brief. Every section is plain markdown
    text (no headers inside; the renderer owns structure). Inline citations
    use [n] matching sources."""
    title: str
    question: str
    executive_summary: str = Field(description="Verdict in the first sentence, then 3 short supporting bullets")
    question_and_why_now: str
    market_landscape: str
    competitive_dynamics: str
    frio_position: str
    strategic_options: list[StrategicOption]
    recommendation_and_next_steps: str
    risks_and_open_questions: str
    sources: list[Source]
