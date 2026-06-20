from core.banner import show_banner
from core.chat import chat_loop
from core.memory import init_db

def main():
    init_db()
    show_banner()
    chat_loop()

if __name__ == "__main__":
    main()
