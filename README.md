# IteraCompute Pricing CLI

Prints a live price table straight from the public API — the same numbers we quote in marketing, so claims and reality never drift.

```bash
python3 scripts/fetch_pricing.py            # terminal table
python3 scripts/fetch_pricing.py --md       # markdown table (paste into docs)
```

Data source: `https://api.iteracompute.com/v1/models` (no auth required).

Output columns: model, quantization, max context, input $/M, cached-input $/M, output $/M, max output.
