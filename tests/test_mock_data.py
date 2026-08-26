import csv, json
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

def test_sales_csv_shape_and_story():
    rows = list(csv.DictReader(open(DATA / "sales_by_category.csv")))
    assert len(rows) == 48  # 6 categories x 8 quarters
    cats = {r["category"] for r in rows}
    assert "Functional (Volt Focus pilot)" in cats
    func_latest = [r for r in rows if r["category"].startswith("Functional") and r["quarter"] == "2026-Q2"][0]
    csd_latest = [r for r in rows if r["category"] == "Carbonated Soft Drinks" and r["quarter"] == "2026-Q2"][0]
    assert float(func_latest["yoy_growth_pct"]) > 30   # punchline: functional booming
    assert abs(float(csd_latest["yoy_growth_pct"])) < 3  # punchline: core flat
    assert float(func_latest["gross_margin_pct"]) > float(csd_latest["gross_margin_pct"])

def test_brand_portfolio():
    brands = json.load(open(DATA / "brand_portfolio.json"))["brands"]
    assert len(brands) >= 10
    assert all({"name", "category", "positioning", "price_tier", "distribution_reach"} <= set(b) for b in brands)

def test_strategy_memo_mentions_key_topics():
    memo = (DATA / "strategy_memo_2025.md").read_text()
    for phrase in ["functional", "cannibalization", "build", "acquire"]:
        assert phrase.lower() in memo.lower()
