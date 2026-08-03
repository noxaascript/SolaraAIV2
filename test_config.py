import unittest

from config import PROVIDERS


class TestModelCatalog(unittest.TestCase):
    def test_catalog_is_simple_and_coding_focused(self):
        self.assertEqual(
            set(PROVIDERS),
            {"qwen", "qwen_72b", "kimi_26", "kimi_25", "llama", "mistral", "deepseek"},
        )
        for provider in PROVIDERS.values():
            self.assertEqual(provider["backend"], "hf")
            self.assertIn("/", provider["model"])


if __name__ == "__main__":
    unittest.main()