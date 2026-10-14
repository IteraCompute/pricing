import contextlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("pricing", Path(__file__).resolve().parents[1] / "scripts/fetch_pricing.py")
pricing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pricing)


class PricingTests(unittest.TestCase):
    def render(self, model):
        response = io.BytesIO(json.dumps({"data": [model]}).encode())
        with patch.object(pricing.urllib.request, "urlopen", return_value=response), patch.object(sys, "argv", ["fetch_pricing.py", "--md"]), contextlib.redirect_stdout(io.StringIO()) as output:
            pricing.main()
        return output.getvalue()

    def test_catalog_only_does_not_claim_free(self):
        result = self.render({"id": "paid/model"})
        self.assertIn("paid/model | ? | N/A | N/A | N/A | N/A | N/A", result)
        self.assertNotIn("$0.00", result)

    def test_real_zero_and_nonzero_prices(self):
        result = self.render({"id": "test/model", "input_modalities": [{"pricing": [{"type": "prompt", "cost_usd": 0}, {"type": "cached_prompt", "cost_usd": 0.000001}]}], "output_modalities": [{"type": "text", "pricing": [{"type": "completion", "cost_usd": 0.000002}]}]})
        self.assertIn("$0.00 | $1.00 | $2.00", result)


if __name__ == "__main__":
    unittest.main()
