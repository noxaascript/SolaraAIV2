from core.web_generator import generate_website
from core.web_memory import save_web_project
from core.deploy_system import (
    deploy_vercel,
    deploy_flask,
    deploy_infinityfree
)


def create_website_project(name, prompt):
    # 1. generate file website
    files = generate_website(name, prompt)

    # 2. simpan ke WebMemory
    save_web_project(
        name=name,
        prompt=prompt,
        files=files,
        platform="auto"
    )

    return {
        "status": "success",
        "name": name,
        "files": list(files.keys())
    }


def deploy_project(name, platform):
    path = f"workspaces/{name}"

    if platform == "vercel":
        return deploy_vercel(path)

    if platform == "flask":
        return deploy_flask(name, {})

    if platform == "infinityfree":
        return deploy_infinityfree(path)

    return "Invalid platform"
