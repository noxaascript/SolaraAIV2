memory_store = []


def add_memory(user, prompt, response, score=1):

    memory_store.append({
        "user": user,
        "prompt": prompt,
        "response": response,
        "score": score
    })

    if len(memory_store) > 100:
        memory_store.pop(0)


def get_memory(limit=5):

    sorted_mem = sorted(
        memory_store,
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_mem[:limit]


def boost_memory(index):

    if index < len(memory_store):
        memory_store[index]["score"] += 1
