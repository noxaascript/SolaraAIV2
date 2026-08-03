import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.code_output import save_generated_code


class TestCodeOutput(unittest.TestCase):
    def test_saves_fenced_code_inside_generated_folder(self):
        response = "Here is the code:\n```python\nprint('hello')\n```"
        with tempfile.TemporaryDirectory() as directory:
            with patch("core.code_output.OUTPUT_DIR", Path(directory) / "generated_code"):
                result = save_generated_code("make a hello script", response)
                output_dir = Path(directory) / "generated_code"
                files = list(output_dir.iterdir())
                self.assertEqual(len(files), 1)
                self.assertEqual(files[0].suffix, ".py")
                self.assertEqual(files[0].read_text(), "print('hello')\n")

        self.assertIn("Saved coded file:", result)

    def test_leaves_normal_response_unchanged(self):
        response = "A function is a reusable block of code."
        self.assertEqual(save_generated_code("explain functions", response), response)


if __name__ == "__main__":
    unittest.main()