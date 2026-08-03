import unittest
from unittest.mock import patch

from providers.router import run_ai


class TestProviderFallback(unittest.TestCase):
    def test_unsupported_model_falls_back_to_qwen(self):
        unsupported = "✖ [400] Bad Request: This model is not available through the selected Hugging Face provider."
        with patch("providers.router.ask_hf", side_effect=[unsupported, "fallback response"]) as ask:
            result = run_ai("qwen_72b", "hello", api_key="hf_test_token")
        self.assertIn("fallback response", result)
        self.assertIn("used Qwen/Qwen2.5-7B-Instruct", result)
        self.assertEqual(ask.call_count, 2)


if __name__ == "__main__":
    unittest.main()