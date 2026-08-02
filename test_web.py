import unittest

from web.app import app


class TestWebAPI(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_healthcheck(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_rejects_invalid_payload(self):
        response = self.client.post("/api/chat", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_exit_command(self):
        response = self.client.post("/api/chat", json={"message": "/exit"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["exit"])


if __name__ == "__main__":
    unittest.main()