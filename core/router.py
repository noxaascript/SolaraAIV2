from core.commands import run_tool

def route(user_input):

    if user_input.startswith("/"):
        return run_tool(user_input)

    return "AI response placeholder"
