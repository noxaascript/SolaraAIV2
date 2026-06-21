memory_store = []


def add_memory(user, prompt, response):

    memory_store.append({
        "user": user,
        "prompt": prompt,
        "response": response
    })

    if len(memory_store) > 50:
        memory_store.pop(0)


def get_memory(limit=5):

    return memory_store[-limit:]
