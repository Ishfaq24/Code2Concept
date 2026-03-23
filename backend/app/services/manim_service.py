import subprocess

import os

def save_code(code: str):
    file_path = "generated/scene.py"

    # 🔥 Ensure directory exists
    os.makedirs("generated", exist_ok=True)

    # 🔥 ALWAYS overwrite
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

def render_video():
    subprocess.run([
        "manim",
        "generated/scene.py",
        "DemoScene",
        "-pql"
    ])