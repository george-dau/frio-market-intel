# Design: Frio Market Intelligence Brief

A multi-agent deep research system built on CrewAI for the FDE take-home
(Option 1: Deep Research Agent). It turns a natural-language market question
from an executive into a cited, board-ready research brief by combining live
external research with the customer's internal data.

## Customer scenario

**Frio Beverage Company** is a fictional Fortune-500-scale CPG beverage
manufacturer headquartered in San Antonio, TX. All "internal" data in this
repo is synthetic, modeled on real public category trends so the numbers are
plausible. In a real engagement this data lives behind the customer's
firewall; a fictional customer is used here deliberately so no real
company's internal figures are fabricated.

The engagement story: Frio's strategy team takes two to three weeks to
answer a market question, so decisions land on stale data. This system
compresses that cycle to minutes and makes it self-serve for executives.

**Demo question:** "Should we enter the functional beverage category?"

The system is question-generic: any market/entry/investment question runs
through the same flow and produces the same report structure.

## Architecture

A CrewAI **Flow** (`MarketBriefFlow`) orchestrates crews. The flow topology
is fixed; agents work inside it.

```
                       @start
              intake: question -> typed state
                     /            \
        (parallel)  /              \  (parallel)
   External Research Crew      Internal Insights Agent
   1. Market Researcher        3. Internal Analyst
      (Serper search +            (file readers over data/:
       web scrape)                 CSV, JSON, markdown)
   2. Market Analyst
      (no tools; insight
       layer over findings)
                    \              /
              @listen(and_(external, internal))
                          |
                  Synthesis Crew
                  4. Strategy Writer
                     (no tools; output_pydantic=ExecutiveBrief)
                          |
               deterministic renderer
              markdown (reports/) + branded HTML
```

Four agents total, deliberately small: each agent exists because specific
report sections require it, and nothing else does.

| Agent | Branch | Tools | Feeds report sections |
|---|---|---|---|
| Market Researcher | external | Serper search, scrape | 3, 4 (raw cited findings) |
| Market Analyst | external | none | 3, 4 (insight layer) |
| Internal Analyst | internal | CSV/JSON/text file readers | 2, 5 |
| Strategy Writer | synthesis | none | all (populates the schema) |

Design notes:

- **Heterogeneous parallel branches.** The fan-out is two different kinds of
  research (open-ended web vs bounded internal files) merged with `and_()`,
  not N copies of the same crew. Combining internal and external data is the
  point of the system, and the topology states it.
- **Asymmetry is deliberate.** The external branch is a two-agent crew
  because open-ended web research benefits from a gather/analyze split. The
  internal branch is a single agent because bounded file analysis does not
  need a crew's overhead.
- **Config where the customer tunes, code where the contract lives.** The
  research crew's agents and tasks are defined in JSONC config files
  (CrewAI's current recommended convention: `crew.jsonc` + per-agent
  config, loaded with `load_crew`), so non-engineers can tune an analyst's
  instructions without touching code. The synthesis crew is defined in
  Python, because it carries the deterministic report contract
  (`output_pydantic=ExecutiveBrief`) that must not drift.

## Deterministic vs non-deterministic

The core design stance: **agents decide what to say; they never decide what
happens next.** Structure is deterministic, content is probabilistic, and
the schema is the contract between them.

Deterministic (identical every run):
- Flow topology (`@start`, parallel branches, `and_()` merge). A run cannot
  skip a branch or loop.
- Typed Pydantic flow state; every inter-step handoff is validated
  structure, not loose prose.
- The report contract: `output_pydantic=ExecutiveBrief`. The writer fills
  seven typed fields; it cannot change the shape. Validation failure
  triggers framework retry.
- Rendering: markdown/HTML generation, citation numbering, branding. No LLM
  involvement.
- Internal inputs: static files, so the internal evidence base is stable.

Non-deterministic (varies per run):
- Search queries issued and sources selected (and the web itself).
- Analyst reasoning: which patterns are surfaced, how evidence is weighed.
- Synthesis prose and the recommendation.

Deliberately unused: CrewAI's `@router` (LLM-driven branching). This use
case has no control-flow decision that should be delegated to a model. In
production a router would gate off-topic questions into clarification.

## Report template (the product)

The deliverable is the **Frio Market Intelligence Brief**, a Pydantic model
(`ExecutiveBrief`) with seven sections, rendered identically on every run:

1. **Executive Summary** - the verdict in the first three lines, then three
   supporting bullets (market signal, internal signal, timing/risk). BLUF:
   an exec who reads nothing else gets the answer.
2. **The Question & Why Now** - the ask restated in business terms; cites
   internal history (the 2025 memo that tabled this question) and what has
   changed since.
3. **Market Landscape** (external) - category size, growth, sub-segments,
   consumer drivers. Web-cited.
4. **Competitive Dynamics** (external) - who moved and how; the pattern the
   moves reveal.
5. **Frio's Position** (internal) - portfolio performance by category;
   launchable assets (brands, distribution). The section no external-only
   tool could write.
6. **Strategic Options** - build / buy / partner compared on speed, cost,
   risk, asset fit; one recommended, reasoning stated.
7. **Recommendation & Next Steps** - verdict restated, phased 90-day plan,
   plus Risks & Open Questions (what the system does not know).

Citations are numbered inline throughout: web sources with URLs, internal
sources by filename. The visible mix of citation types is the
internal+external story on every page.

## Mock internal data (`data/`)

Three files, three ingestion shapes (structured CSV, structured JSON,
unstructured text):

1. `sales_by_category.csv` - 8 quarters x category (CSD, juice, water,
   sports, tea/coffee, one small experimental functional SKU line):
   revenue, volume, YoY growth, gross margin. Story the data tells: core
   flat (~1%), functional line growing ~40% off a small base.
2. `brand_portfolio.json` - ~12 fictional brands: category, positioning,
   price tier, target demographic, distribution reach. Makes the
   recommendation actionable ("launch via your sports brand and cold-chain
   distribution").
3. `strategy_memo_2025.md` - one-page internal memo that considered
   functional beverages last year and tabled the decision (cannibalization
   risk, build-vs-buy unresolved). Lets the brief open with "this was
   raised internally and deferred; here is what changed."

## Delivery surfaces

Identical report content on every surface; only the surface changes.

1. Markdown committed to `reports/` (renders on GitHub; the reproducible
   graded artifact).
2. Branded static HTML via a small deterministic renderer (what an exec
   would actually be handed).
3. CrewAI AMP deployment (free org): kickoff via the platform's Run tab,
   execution visible in the Traces tab. Optional per the assignment;
   included because it is how the system would actually be operated.
4. CLI: `uv run kickoff --question "..."` runs everything locally with no
   platform account.

## Stack

- Python 3.12+, uv for env/deps
- `crewai` + `crewai-tools`
- Search: Serper (free tier)
- LLM: provider-agnostic via env configuration (CrewAI/LiteLLM convention).
  Shipped default: OpenAI's mini tier; `.env.example` includes commented
  alternatives (Anthropic Claude Haiku 4.5, Google Gemini Flash), any of
  which works with the same code. Rationale: model choice matters less
  than system design; a cost-effective mini-class model is sufficient when
  the structure carries the quality, and swapping is a one-line env
  change. Direct provider keys by design: enterprise deployments get model
  flexibility through their cloud provider (Bedrock/Vertex/Azure) or
  direct contracts, not third-party proxies.
- No database, no custom UI. Secrets via `.env` (`.env.example` committed).

## Error handling (prototype-appropriate)

- Schema validation failures: retried by the framework via
  `output_pydantic`.
- Search/tool failures: surfaced clearly and fail the run fast; no silent
  partial reports. A report missing a branch is worse than no report.
- Reproducibility hedge: the internal branch is fully deterministic, so
  evaluator runs always produce a sensible Frio's Position section even if
  the day's web results differ.

## Testing

- Unit tests for the deterministic shell: report rendering from a fixture
  `ExecutiveBrief`, data-file loaders, citation numbering.
- One committed sample report generated end-to-end (the assignment's
  required artifact) serving as the reference output.
- Agent quality is validated by inspection of the sample report, not
  automated evals; that trade-off is stated in the README.

## Out of scope (deliberate)

- Databases, vector stores, RAG infrastructure (three small files do not
  need retrieval).
- `@persist()` / human-in-the-loop checkpoints (production feature; noted
  in path-to-production).
- LLM-as-judge / automated eval harness.
- Custom web UI (the AMP platform provides the operator surface).
- Chart generation in the report (markdown tables suffice; stretch goal).

## Path to production (README summary)

What would change for a real deployment: internal connectors (warehouse,
SharePoint/Drive, BI exports) behind the customer's firewall instead of
static files; an HITL checkpoint where an analyst reviews sources before
synthesis; scheduled and event-triggered runs (competitive monitoring);
report template variants per audience (deck, email digest); observability
and cost controls via the platform; SSO/RBAC. The Flow, crews, and report
contract are unchanged: the reusable core is the orchestration pattern plus
the schema, and the swappable edges are tools and templates.
