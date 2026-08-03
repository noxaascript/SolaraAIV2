memory_store = []


def add_memory(user, prompt, response, score=1):

    memory_store.append({
        "user": user,
        "prompt": prompt,
        "response": response,
        "score": score
    })

    if len(memory_store) > 200:
        memory_store.pop(0)


def get_memory(limit=5):

    # ambil yang paling relevan (skor tinggi + recent)
    sorted_mem = sorted(
        memory_store,
        key=lambda x: (x["score"], len(x["prompt"])),
        reverse=True
    )

    return sorted_mem[:limit]


# =========================
# AUTO IMPROVE MEMORY SCORE
# =========================
def improve_memory(user_input):

    keywords = user_input.lower().split()

    for mem in memory_store:

        match = 0

        for k in keywords:

            if k in mem["prompt"].lower():
                match += 1

        if match >= 2:
            mem["score"] += 1
