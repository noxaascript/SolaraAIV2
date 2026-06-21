import subprocess

def run_file(file):
    p = subprocess.run(
        ["python", file],
        capture_output=True,
        text=True
    )

    return p.returncode, p.stdout, p.stderr
