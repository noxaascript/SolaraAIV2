import unittest

from core.hf_credentials import (
    clear_user_key,
    get_user_key,
    has_user_key,
    set_user_key,
)


class TestRuntimeHuggingFaceCredentials(unittest.TestCase):
    def tearDown(self):
        clear_user_key("test-user")

    def test_accepts_valid_key_without_persisting_to_disk(self):
        self.assertTrue(set_user_key("test-user", "hf_example_token"))
        self.assertTrue(has_user_key("test-user"))
        self.assertEqual(get_user_key("test-user"), "hf_example_token")

    def test_rejects_invalid_key(self):
        self.assertFalse(set_user_key("test-user", "not-a-token"))
        self.assertFalse(has_user_key("test-user"))


if __name__ == "__main__":
    unittest.main()