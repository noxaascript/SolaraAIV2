def choose_model(message):
    text = message.lower()

    coding_words = [
        "code", "coding", "program", "python", "javascript",
        "html", "css", "bug", "error", "website", "api",
        "database", "sql", "app", "function", "script"
    ]

    reasoning_words = [
        "explain", "why", "how", "compare", "analysis",
        "think", "strategy", "science", "math", "theory",
        "concept", "meaning", "difference"
    ]

    chat_words = [
        "hi", "hello", "halo", "hey", "sup", "apa kabar"
    ]

    for w in coding_words:
        if w in text:
            return "coding"

    for w in reasoning_words:
        if w in text:
            return "reasoning"

    for w in chat_words:
        if w in text:
            return "fast"

    return "fast"
