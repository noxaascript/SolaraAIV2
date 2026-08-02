@@
-        if res.status_code == 401:
-            return "x  Invalid OPENAI_API_KEY. Get one: platform.openai.com/api-keys"
-        if res.status_code == 429:
-            return "x  OpenAI rate limit hit. Wait a moment and try again."
-        if res.status_code == 404:
-            return f"x  Model '{model}' not found. Check: platform.openai.com/docs/models"
-        if res.status_code != 200:
-            return f"x  OpenAI error {res.status_code}: {res.text[:200]}"
+        from core.error_utils import format_error
+        if res.status_code == 401:
+            return format_error(401, "Invalid OPENAI_API_KEY. Get one: platform.openai.com/api-keys")
+        if res.status_code == 429:
+            return format_error(429, "OpenAI rate limit hit. Wait a moment and try again.")
+        if res.status_code == 404:
+            return format_error(404, f"Model '{model}' not found. Check: platform.openai.com/docs/models")
+        if res.status_code != 200:
+            return format_error(res.status_code, res.text[:200])
@@
-    except requests.exceptions.Timeout:
-        return "x  Timed out (60s). Try /model to switch to a faster model."
-    except Exception as e:
-        return f"x  Connection failed: {str(e)[:200]}"
+    except requests.exceptions.Timeout:
+        from core.error_utils import format_error
+        return format_error(504, "Timed out (60s). Try /model to switch to a faster model.")
+    except Exception as e:
+        from core.error_utils import format_error
+        return format_error(502, f"Connection failed: {str(e)}")
