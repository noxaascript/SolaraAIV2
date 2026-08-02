@@
-        if res.status_code == 503:
-            return "⏳  Model is warming up (~20 sec). Try again in a moment."
-        if res.status_code == 401:
-            return (
-                "✖  Invalid HF_API_KEY.\n"
-                "   Get a free key: huggingface.co/settings/tokens"
-            )
-        if res.status_code == 429:
-            return "✖  Rate limited. Wait a moment and try again."
-        if res.status_code != 200:
-            return f"✖  HF error {res.status_code}: {res.text[:200]}"
+        from core.error_utils import format_error
+
+        if res.status_code == 503:
+            return format_error(503, "Model is warming up (~20 sec). Try again in a moment.")
+        if res.status_code == 401:
+            return format_error(401, "Invalid HF_API_KEY. Get a free key: huggingface.co/settings/tokens")
+        if res.status_code == 429:
+            return format_error(429, "Rate limited. Wait a moment and try again.")
+        if res.status_code != 200:
+            # Return the HTTP status code with a snippet of the response
+            return format_error(res.status_code, res.text[:200])
@@
-    except requests.exceptions.Timeout:
-        return (
-            "✖  Timed out (60s).\n"
-            "   Try a faster model: /model  →  phi or mistral"
-        )
-    except Exception as e:
-        return f"✖  Connection failed: {str(e)[:200]}"
+    except requests.exceptions.Timeout:
+        from core.error_utils import format_error
+        return format_error(504, "Timed out (60s). Try a faster model or run locally.")
+    except Exception as e:
+        from core.error_utils import format_error
+        return format_error(502, f"Connection failed: {str(e)}")
