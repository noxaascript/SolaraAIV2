SolaraAI

Solara AI OS is a modular AI system combining:
- Multi-model AI (Qwen / Kimi / Groq / LLaMA)
- Custom Brain Core
- BrowserOS (AI web browsing system)
- Memory system
- Terminal-based UI OS

---

# 🧠 Features

## ⚙️ AI Core System
- Hybrid model routing (auto choose model)
- Multi-brain system (coder / reasoning / planner)
- Memory with scoring system
- Self-improving context memory

## 🌐 BrowserOS
- Open web pages
- Scrape text content
- AI web summarization
- Session & history tracking

## 🧬 Model Support
- Qwen (HuggingFace API / Transformers)
- Kimi K2.7 Code (local Transformers)
- Groq (optional API)
- LLaMA (optional API)

## 🖥️ UI System
- Terminal OS-style interface
- Dashboard menu
- Live typing AI response
- Loading animations

---

# 📁 Project Structure

SolaraAIV2/ │ ├── core/ │   ├── router.py │   ├── tools.py │   ├── agent_os.py │ ├── model_core/ │   ├── brain.py │   ├── router.py │   ├── memory.py │   ├── prompt.py │   ├── kimi.py │   ├── qwen.py │   ├── config.py │ ├── browser_os/ │   ├── browser.py │   ├── navigator.py │   ├── scraper.py │   ├── memory.py │   ├── agent.py │ ├── ui/ │   ├── terminal_ui.py │   ├── dashboard.py │   ├── chat_ui.py │   ├── loader.py │   ├── typing.py │ ├── main.py └── README.md

---

# 🚀 Installation

## 1. Clone repo
```bash
git clone https://github.com/noxaascript/SolaraAIV2
cd SolaraAIV2

2. Install dependencies

pip install requests beautifulsoup4 transformers torch accelerate
'''bash

--------

🔑 API Setup (optional)

HuggingFace

export HF_API_KEY="your_token_here"

Or edit config directly

HF_API_KEY = "your_token_here"


---

▶️ Run Project

bash start.sh


---

🧠 How It Works

User Input
   ↓
UI Layer (Terminal OS)
   ↓
Router (brain selector)
   ↓
Model Core (Qwen / Kimi / etc)
   ↓
Tools (BrowserOS / memory / code tools)
   ↓
Final Response


---

🤖 Model Routing Logic

Input Type	Model

Coding	Kimi K2.7 Code
Reasoning	Kimi / Qwen
Chat	Qwen
General	Groq (optional)



---

🌐 BrowserOS Flow

AI Agent
   ↓
Navigator
   ↓
Browser Fetch
   ↓
Scraper
   ↓
Memory Store
   ↓
AI Summary


---

⚡ UI Features

Live typing AI response

OS-style dashboard

Loading animation

Clean chat display



---

🧬 Future Upgrades

Multi-model voting system

Autonomous web agent

Self-editing code engine

Visual browser mode (Playwright)

GUI / Web version (Glass UI)



---

⚠️ Notes

Kimi model is heavy (not recommended for low RAM devices)

HuggingFace API may have latency

BrowserOS V1 uses requests (no real browser engine yet)



---

💀 Warning

This system is experimental AI architecture. Expect bugs, crashes, and rapid evolution.


---

🔥 Author

Built as a modular AI OS experiment:

Brain Core System

Multi-model AI routing

Browser + Dev automation system


---
