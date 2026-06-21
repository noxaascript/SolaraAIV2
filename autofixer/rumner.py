import subprocess

def run_file(file):
    result = subprocess.run(
        ["python", file],
        capture_output=True,
        text=True
    )

    return result.returncode, result.stdout, result.stderr
