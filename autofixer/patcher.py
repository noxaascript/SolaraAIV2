from config import AUTO_APPLY

def apply_patch(ai_output):
    """
    Parse output AI dan apply ke file
    """

    if not AUTO_APPLY:
        print("\n🧠 PATCH PREVIEW (AUTO APPLY OFF)\n")
        print(ai_output)
        return

    blocks = ai_output.split("FILE:")

    for b in blocks:
        if "CODE:" not in b:
            continue

        try:
            path = b.split("\n")[0].strip()
            code = b.split("CODE:")[1].strip()

            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            print(f"✔ patched: {path}")

        except Exception as e:
            print(f"❌ patch failed: {str(e)}")
