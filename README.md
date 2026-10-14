# IteraCompute Pricing CLI

Inspect the public IteraCompute model catalog and any pricing metadata returned by the API. Uses Python 3 and the standard library; no API key or pip dependencies are required.

```sh
git clone https://github.com/IteraCompute/pricing.git
cd pricing
```

```bash
python3 scripts/fetch_pricing.py            # terminal table
python3 scripts/fetch_pricing.py --md       # markdown table (paste into docs)
```

Data source: `https://api.iteracompute.com/v1/models` (no auth required).

Output columns: model, quantization, max context, input $/M, cached-input $/M, output $/M, max output.

Missing prices and limits are shown as `N/A`, not zero. The current gateway can return model IDs without pricing metadata; `N/A` does not mean a model is free. Check [official pricing](https://iteracompute.com/pricing/) and [API documentation](https://iteracompute.com/docs.html) for published rates and access rules.

On Windows PowerShell use `python` instead of `python3`. Network errors require connectivity to `api.iteracompute.com`; retry after a delay.

To make your first free Qwen call or run a complete application, use [migration-kit](https://github.com/IteraCompute/migration-kit).

Offline checks: `python3 -m unittest discover -s tests -v`.
