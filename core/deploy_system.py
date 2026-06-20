import os
import subprocess


def deploy_vercel(path):
    return subprocess.getoutput(f"cd {path} && vercel --prod --yes")


def deploy_flask(name, files):
    path = f"flask_apps/{name}"
    os.makedirs(path, exist_ok=True)

    main_py = f"""
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''{files.get("index.html", "")}'''

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
"""

    with open(os.path.join(path, "app.py"), "w") as f:
        f.write(main_py)

    return f"Flask app created at {path}"


def deploy_infinityfree(path):
    return f"Upload {path} via FTP to InfinityFree (manual step)"
