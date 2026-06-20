from providers.smart_router import auto_chat


def create_plan(prompt, user_id):

    return auto_chat(f"""
You are an AI planner in a dev OS.

Break this task into simple executable steps:

Task: {prompt}

Rules:
- short steps
- executable actions only
- no explanation

Return list format.
""")
