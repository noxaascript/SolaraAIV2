from Core import router

def run_core(user_input):
    try:
        return router.handle_input(user_input)
    except Exception as e:
        return f"[CORE ERROR] {str(e)}"
