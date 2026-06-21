# ======================================
# SOLARA AI V2 - Router System
# ======================================

from providers.qwen import ask_qwen
from providers.kimi import ask_kimi


def router(prompt, model="auto"):
    """
    Solara AI Router
    Decide which AI model should answer.
    """

    prompt_lower = prompt.lower()

    try:
        # Auto routing
        if model == "auto":

            coding_keywords = [
                "code",
                "python",
                "script",
                "error",
                "bug",
                "fix",
                "debug",
                "program"
            ]

            if any(word in prompt_lower for word in coding_keywords):
                return ask_kimi(prompt)

            return ask_qwen(prompt)

        # Manual model selection
        elif model == "qwen":
            return ask_qwen(prompt)

        elif model == "kimi":
            return ask_kimi(prompt)

        else:
            return "⚠ Unknown model selected."

    except Exception as e:
        return f"⚠ Router Error: {str(e)}"


# Test router
if __name__ == "__main__":
    while True:
        text = input("Test > ")

        if text.lower() == "exit":
            break

        print(router(text))
