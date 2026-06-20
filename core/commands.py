from core.workspace import (
    create_workspace,
    list_workspaces,
    read_workspace,
    add_file,
    auto_app
)

from core.website_pipeline import create_web_project


def run_tool(user_input):
    cmd = user_input.strip().lower()

    # HELP
    if cmd == "/help":
        return "/workspace create/list/open/addfile | /web create"

    # WORKSPACE
    if cmd.startswith("/workspace create"):
        name = cmd.split()[2]
        return create_workspace(name)

    if cmd == "/workspace list":
        return "\n".join(list_workspaces())

    if cmd.startswith("/workspace open"):
        name = cmd.split()[2]
        return str(read_workspace(name))

    if cmd.startswith("/workspace addfile"):
        parts = cmd.split()
        return add_file(parts[2], parts[3], " ".join(parts[4:]))

    if cmd.startswith("/workspace ai"):
        parts = cmd.split()
        return auto_app(parts[3], " ".join(parts[4:]))

    # WEB
    if cmd.startswith("/web create"):
        parts = cmd.split()
        return create_web_project(parts[2], " ".join(parts[3:]))

    return None
