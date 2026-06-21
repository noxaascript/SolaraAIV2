# 🤖 SolaraAINEW

SolaraAINEW is a modular AI Operating System that combines multiple AI models, a browser automation system, and a terminal-based interface into a single unified runtime.

The system is designed to act like a lightweight AI operating environment where different models can be selected dynamically depending on the type of task. It supports coding, reasoning, general conversation, and planning workflows through a routing system that distributes tasks to different AI brains.

It also includes a memory layer that stores past interactions, allowing the system to maintain context over time and improve response relevance.

This project is experimental and focused on building an AI architecture that behaves like a mini operating system inside a terminal.

---

## ⚡ Installation

Start by cloning the repository:

```bash
git clone https://github.com/noxaascript/SolaraAIV2

Move into the project directory:

cd SolaraAIV2/SolaraAINEW

Install required dependencies:

pip install requests beautifulsoup4 transformers torch accelerate

If you are using HuggingFace models that require authentication, set your token:

export HF_API_KEY="your_huggingface_token"


---

🚀 Running the System

To start the AI system, run:

bash start.sh

If you prefer running directly with Python, use:

python main.py

The system will launch a terminal-based interface where you can interact with the AI.


---

🧠 System Behavior

When the system is running, user input goes through several stages:

1. Input is received from the terminal interface


2. A router analyzes the input type (chat, coding, reasoning, planning)


3. The appropriate AI model is selected automatically


4. The selected model generates a response


5. Optional tools such as browser or memory system may be activated


6. The final response is displayed back in the terminal



This allows the system to behave like a multi-agent AI environment rather than a single static model.


---

🤖 Model Handling

The system can work with multiple AI backends:

Qwen models for general conversation and reasoning

Kimi models for coding-related tasks

Optional API-based models such as Groq or LLaMA

A routing layer that automatically selects the best model for the task


Each model is used depending on the input classification from the router system.


---

🌐 Browser Capability

The system includes a lightweight browser module that can:

Fetch web pages using HTTP requests

Extract readable text from HTML content

Pass extracted information into the AI system for summarization or reasoning


This allows the AI to interact with external web content without requiring a full browser engine.


---

⚙️ Requirements

Make sure your system has:

Python 3.10 or higher

pip package manager

Internet connection for model and browser features


Required Python libraries:

pip install requests
pip install beautifulsoup4
pip install transformers
pip install torch
pip install accelerate


---

⚠️ Notes

Some models may require significant system resources, especially transformer-based models such as Kimi.

HuggingFace models may require authentication depending on usage limits.

Browser features are lightweight and not equivalent to a full Chromium-based browser.

This project is still under active development and may change frequently.


---

💀 Disclaimer

This project is built for experimental and educational purposes only. It is not intended for production environments.

Use responsibly.
