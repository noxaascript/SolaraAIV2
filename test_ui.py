import unittest
import sys
from io import StringIO

# Mock standard output so we can capture and assert printed UI structures
from ui.dashboard import _strip_ansi, dashboard, models_menu
from ui.typing import ai_type, user_echo, system_msg, error_msg, success_msg
from ui.terminal_ui import section_banner, help_menu
from core.chat import stream


class TestSolaraUI(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_strip_ansi(self):
        colored_text = "\033[96mHello\033[0m \033[95mWorld\033[0m"
        self.assertEqual(_strip_ansi(colored_text), "Hello World")

    def test_system_messages(self):
        system_msg("Test System")
        error_msg("Test Error")
        success_msg("Test Success")
        
        output = self.held_output.getvalue()
        self.assertIn("[system] Test System", _strip_ansi(output))
        self.assertIn("[error]  Test Error", _strip_ansi(output))
        self.assertIn("[success] Test Success", _strip_ansi(output))

    def test_ai_type_box_structure(self):
        ai_type("Line 1\nLine 2", label="TestAI")
        output = self.held_output.getvalue()
        
        # Check that it has top, left, and bottom borders
        self.assertIn("╭── TestAI", _strip_ansi(output))
        self.assertIn("│  Line 1", _strip_ansi(output))
        self.assertIn("│  Line 2", _strip_ansi(output))
        self.assertIn("╰────────", _strip_ansi(output))

    def test_dashboard_hud(self):
        dashboard(user="test_user", model="gemma", mode="dev")
        output = self.held_output.getvalue()
        
        # Check alignment and parameters
        self.assertIn("USER: test_user", _strip_ansi(output))
        self.assertIn("MODE: dev", _strip_ansi(output))
        self.assertIn("MODEL: gemma", _strip_ansi(output))
        
        # Check HUD borders and width
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        for line in lines:
            stripped = _strip_ansi(line)
            if "╭" in stripped or "╰" in stripped or "├" in stripped:
                # Border line should be 54 characters (2 spaces + 1 border + 52 dash + 1 border)
                self.assertEqual(len(stripped), 54)
            elif "│" in stripped:
                # Row content should align perfectly with the border width
                self.assertEqual(len(stripped), 54)

    def test_section_banner_width(self):
        section_banner("My Title")
        output = self.held_output.getvalue()
        
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        # The horizontal separator line (second line) should have exactly 52 divider characters
        self.assertEqual(len(_strip_ansi(lines[1])), 52)

    def test_help_menu_width(self):
        help_menu()
        output = self.held_output.getvalue()
        
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        # Top and bottom dividers should be 52 characters
        dividers = [line for line in lines if "═" in line]
        for div in dividers:
            self.assertEqual(len(_strip_ansi(div)), 52)


if __name__ == "__main__":
    unittest.main()
