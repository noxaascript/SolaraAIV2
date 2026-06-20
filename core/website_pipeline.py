from core.web_generator import generate_website
from core.website_memory import save_project
from core.deploy_system import (
    deploy_vercel,
    deploy_flask,
    deploy_infinityfree
)
from core.web_memory import save_web_project


def create_website_project(name, prompt):
    files = generate_website(name, prompt)

    save_project(name, prompt, files)

    return {
        "name": name,
        "files": files,
        "status": "created"
    }


def deploy_project(name, platform):
    import os

    path = f"workspaces/{name}"

    if platform == "vercel":
        return deploy_vercel(path)

    if platform == "flask":
        return deploy_flask(name, {})

    if platform == "infinityfree":
        return deploy_infinityfree(path)

    return "Invalid platform"
