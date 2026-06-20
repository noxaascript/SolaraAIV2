import os
import subprocess


def deploy_vercel(path):
    try:
        # assume vercel CLI installed
        cmd = f"cd {path} && vercel --prod --yes"
        result = subprocess.getoutput(cmd)
        return result
    except Exception as e:
        return str(e)


def deploy_static_zip(path):
    zip_path = f"{path}.zip"
    cmd = f"cd workspaces && zip -r {zip_path} {path}"
    subprocess.getoutput(cmd)
    return zip_path
