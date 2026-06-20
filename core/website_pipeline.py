from core.web_generator import generate_website
from core.web_memory import save_web_project, save_to_main_file
from core.workspace import auto_app


def create_web_project(name, prompt):
    files = generate_website(name, prompt)

    save_web_project(name, prompt, files)
    save_to_main_file(name, prompt, files)

    auto_app(name, prompt)

    return "File Web tersimpan di WebMemory/web.txt"
