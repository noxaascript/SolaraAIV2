from V2.core_bridge import call_core

def run_core(user_input):
    try:
        return call_core(user_input)
    except Exception as e:
        return f"[CORE ERROR] {str(e)}"
