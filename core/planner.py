from providers.smart_router import auto_chat


def create_plan(prompt):

    return auto_chat(f"""
You are AI Dev OS Planner with Browser access.

If task needs information:
- use browser_visit
- use browser_summary

Break task into steps:

Task:
{prompt}

Return ONLY steps.
""")
