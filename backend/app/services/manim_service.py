import subprocess

def save_code(code: str):
    with open("generated/scene.py", "w") as f:
        f.write(code)

def render_video():
    subprocess.run([
        "manim",
        "generated/scene.py",
        "DemoScene",
        "-pql"
    ])