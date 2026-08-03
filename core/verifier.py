from providers.smart_router import auto_chat

def verify_result(prompt, result, user_id=None):
    return result
    
    return auto_chat(f"""
You are a system verifier in AI Dev OS.

User task:
{prompt}

Execution result:
{result}

Check:
- is task completed?
- if not, explain missing parts
- give final clean answer

Return final output only.
""")
