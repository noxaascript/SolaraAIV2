from Core import router

def run_core(user_input):
    """
    bridge V2 → Core lama
    """

    try:
        return router.handle_input(user_input)

    except Exception as e:
        return f"[CORE ERROR] {str(e)}"
