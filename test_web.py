import unittest
from unittest.mock import patch

from web.app import app


class TestWebAPI(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        with self.client.session_transaction() as state:
            state["auth_user"] = {"id": "test-user", "email": "test@example.com", "name": "Test User"}

    def test_healthcheck(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_auth_status(self):
        response = self.client.get("/api/me")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["authenticated"])

    def test_logout_clears_auth_session(self):
        response = self.client.get("/auth/logout")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.get("/api/me").get_json()["authenticated"])

    def test_status_never_exposes_key(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("huggingface_key_configured", payload)
        self.assertNotIn("HF_API_KEY", payload)
        self.assertNotIn("token", str(payload).lower())

    def test_supabase_supports_publishable_key_name(self):
        with self.client.session_transaction():
            pass
        with patch.dict("os.environ", {"SUPABASE_URL": "https://example.supabase.co", "SUPABASE_PUBLISHABLE_KEY": "public-key", "SUPABASE_ANON_KEY": ""}):
            from web.app import _supabase_configured
            self.assertTrue(_supabase_configured())

    def test_web_hf_key_setup_uses_session_only(self):
        response = self.client.post("/api/hf-key", json={"key": "hf_example_token"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["ok"])
        status = self.client.get("/api/status").get_json()
        self.assertTrue(status["huggingface_key_configured"])
        self.assertNotIn("hf_example_token", str(status))
        cleared = self.client.delete("/api/hf-key")
        self.assertEqual(cleared.status_code, 200)

    def test_hf_key_command_is_documented_by_secure_endpoint(self):
        response = self.client.post("/api/hf-key", json={"key": "not-valid"})
        self.assertEqual(response.status_code, 400)


    def test_rejects_invalid_payload(self):
        response = self.client.post("/api/chat", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_exit_command(self):
        response = self.client.post("/api/chat", json={"message": "/exit"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["exit"])

    def test_identity_question(self):
        response = self.client.post("/api/chat", json={"message": "Who are you?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["message"],
            "I'm SolaraAI, made by KareemXD. I'm using models like Qwen and others.",
        )

    def test_generated_file_download_route_rejects_missing_file(self):
        response = self.client.get("/api/generated-files/not-created.py")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()