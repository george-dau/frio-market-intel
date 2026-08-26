# CrewAI FDE Take-Home — Brief (extracted from `FDE Take-Home Assessment.pdf`)

Simulates a real customer engagement: design, build, and present an AI-powered
multi-agent solution the way an FDE would.

## Scenario options

**Option 1 (primary) — Deep Research Agent.** Gathers external (public internet)
and internal (mocked static files) information and combines them into an
executive-ready report on a topic (industry, market/technology area, investment
opportunity). Identify what's changing, how leaders innovate, who the new
entrants are, where investment is flowing.

**Option 2 (alternatives, drawn from real CrewAI engagements)** — pick one:
- Document validation & compliance crew — classify a document bundle (permits,
  IDs, contracts), extract key fields, cross-check consistency, return
  approve / flag-for-review with a full audit trail.
- Vendor & sourcing recommendation agent — given item, quantity, location, query
  multiple mocked systems for availability/cost/lead time, return a ranked,
  margin-aware recommendation with rationale.
- RFP / proposal response generator — given an RFP plus a mocked internal
  knowledge base, draft structured cited responses per requirement, flag gaps,
  produce a client-ready document.

## Technical expectations
- **Framework:** CrewAI suggested (clean path to CrewAI Enterprise). Other
  frameworks/SDKs allowed — be ready to defend the choice and say what would
  change for production.
- **LLM:** system design matters more than model. Simple, cost-effective,
  multimodal-capable model is fine; defend it simply.
- **Data:** public internet where it helps (don't spend money); mock internal
  data with static JSON/CSV in the repo. No hosted DB needed.
- **Output:** a defined structured report template the agents populate
  consistently — clear, structured, actionable for a business exec.
- **Optional, ungraded:** deploy to CrewAI platform for traces.

## Deliverables
1. **Working code repo (50%)** — zip of the complete solution, clear README
   (setup, architecture overview, design decisions), runnable/reproducible code,
   and at least one sample generated report committed in the repo.
2. **Customer-facing demo video (50%)** — 3–5 min screen recording with
   voiceover, presented as if delivering to a VP of AI at a Fortune 500.
   Shared via link (Loom / Drive / unlisted YouTube).

## Timeline
Within 3 days of receipt (extension available on request).

## Evaluation
- Solution architecture and technology choices; how internal + external data are
  combined; trade-offs you can articulate.
- A working prototype the team can run and reproduce.
- Usefulness and polish of the executive-ready output.
- Clarity, credibility, and presence of the demo.

## Notes
- Prototype, not production — architecture, judgment, and demo over feature
  completeness.
- Hardcoding a showcase demo input is fine. AI coding assistants welcome.
- Keep secrets out of the repo; include `.env.example` and note required keys.
- If something is ambiguous: make a reasonable assumption, note it, move on.

## Submission
Reply to the CrewAI recruiter with repo (zip or link) + demo video link.
