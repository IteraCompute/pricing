#!/usr/bin/env python3
"""Fetch IteraCompute /v1/models and print a pricing table.

Usage:
  python3 fetch_pricing.py          # terminal table
  python3 fetch_pricing.py --md     # markdown table
"""
import json
import sys
import urllib.request

URL = "https://api.iteracompute.com/v1/models"


def per_m(price) -> float:
    return float(price) * 1_000_000


def price_cell(price) -> str:
    return "N/A" if price is None else f"${per_m(price):.2f}"


def main() -> None:
    with urllib.request.urlopen(URL, timeout=30) as r:
        data = json.load(r)["data"]

    rows = []
    for m in data:
        mid = m["id"]
        quant = m.get("quantization", "?")
        ctx = next(
            (
                im["supported_inputs"]["max_context_length"]["value"]
                for im in m.get("input_modalities", [])
                if "max_context_length" in im.get("supported_inputs", {})
            ),
            None,
        )
        out = next(
            (
                om.get("max_length", {}).get("value")
                for om in m.get("output_modalities", [])
                if om.get("type") == "text"
            ),
            None,
        )
        prices = {
            p["type"]: p["cost_usd"]
            for im in m.get("input_modalities", [])
            for p in im.get("pricing", [])
        }
        op = next(
            (
                {p["type"]: p["cost_usd"] for p in om.get("pricing", [])}
                for om in m.get("output_modalities", [])
                if om.get("type") == "text"
            ),
            {},
        )
        rows.append(
            [
                mid,
                quant,
                "N/A" if ctx is None else f"{ctx:,}",
                price_cell(prices.get('prompt')),
                price_cell(prices.get('cached_prompt')),
                price_cell(op.get('completion')),
                "N/A" if out is None else f"{out:,}",
            ]
        )

    header = ["model", "quant", "context", "in $/M", "cached $/M", "out $/M", "max out"]
    if "--md" in sys.argv:
        print("| " + " | ".join(header) + " |")
        print("|" + "---|" * len(header))
        for row in rows:
            print("| " + " | ".join(str(c) for c in row) + " |")
    else:
        widths = [max(len(str(r[i])) for r in [header] + rows) for i in range(len(header))]
        print("  ".join(h.ljust(w) for h, w in zip(header, widths)))
        print("-" * (sum(widths) + 2 * (len(widths) - 1)))
        for row in rows:
            print("  ".join(str(c).ljust(w) for c, w in zip(row, widths)))


if __name__ == "__main__":
    main()
