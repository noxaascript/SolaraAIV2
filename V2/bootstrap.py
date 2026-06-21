from V2.orchestrator.system_router import start_system
from Core import router  # bridge ke sistem lama (kalau dibutuhkan)

def boot():
    print("""
========================
   SOLARA AI V2 BOOT
   ORCHESTRATOR ACTIVE
========================
""")

    start_system()


if __name__ == "__main__":
    boot()
