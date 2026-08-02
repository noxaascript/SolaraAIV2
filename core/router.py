@@
     try:
         response = ask_groq(text)
         return response

     except Exception as e:
-        return f"Router Error: {str(e)}"
+        from core.error_utils import format_error
+        # Use exit code 127 for unexpected command/execution errors where appropriate
+        return format_error(500, f"Router Error: {str(e)}")
