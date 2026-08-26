"""Generates Frio's synthetic sales data. Deterministic: growth trajectories
are parameters modeled on real public category trends (flat CSD, ~40% YoY
functional growth), scaled to a fictional portfolio."""
import csv
from pathlib import Path

OUT = Path(__file__).parent.parent / "data" / "sales_by_category.csv"
QUARTERS = ["2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2"]

# (category, base_revenue_musd, quarterly_growth_rate, gross_margin_pct, musd_per_m_cases)
CATEGORIES = [
    ("Carbonated Soft Drinks",        1180.0,  0.0025, 38.0, 9.5),
    ("Juice & Nectars",                310.0, -0.0075, 31.0, 11.0),
    ("Bottled Water",                  455.0,  0.0100, 22.0, 5.0),
    ("Sports Drinks",                  265.0,  0.0150, 41.0, 12.0),
    ("Tea & Coffee RTD",               190.0,  0.0075, 35.0, 13.0),
    ("Functional (Volt Focus pilot)",   22.0,  0.0875, 52.0, 18.0),
]

def rows():
    for cat, base, g, margin, price in CATEGORIES:
        for i, q in enumerate(QUARTERS):
            rev = base * (1 + g) ** i
            yoy = ((1 + g) ** 4 - 1) * 100  # constant-rate model
            yield {
                "quarter": q, "category": cat,
                "revenue_musd": round(rev, 1),
                "volume_m_cases": round(rev / price, 1),
                "yoy_growth_pct": round(yoy, 1),
                "gross_margin_pct": margin,
            }

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["quarter", "category", "revenue_musd", "volume_m_cases", "yoy_growth_pct", "gross_margin_pct"])
        w.writeheader()
        w.writerows(rows())
    print(f"wrote {OUT}")
