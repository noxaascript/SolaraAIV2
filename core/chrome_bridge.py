@@
 def send_to_chrome(action, data=None):
@@
-    except Exception as e:
-        return {
-            "status": "error",
-            "message": str(e)
-        }
+    except Exception as e:
+        # Return a standardized error string so chat shows codes clearly
+        try:
+            from core.error_utils import format_error
+            return {"status": "error", "message": format_error(502, str(e))}
+        except Exception:
+            return {"status": "error", "message": str(e)}
