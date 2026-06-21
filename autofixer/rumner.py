import subprocess

def run_file(file_path):
    result = subprocess.run(
        ["python", file_path],
        capture_output=True,
        text=True
    )

    return result.returncode, result.stdout, result.stderr
