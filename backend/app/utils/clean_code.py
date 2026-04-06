import re


def clean_code(code: str) -> str:
    """Minimal cleaning and small compatibility fixes"""
    # Strip possible markdown fences
    code = code.replace("```python", "").replace("```", "").strip()

    # Manim Community v0.20.1 does not define the CYAN constant.
    # Replace bare CYAN usage with an explicit hex color so generated
    # code doesn't crash at runtime with NameError.
    code = re.sub(r"\bCYAN\b", '"#00FFFF"', code)

    return code

def validate_manim_code(code: str) -> tuple[bool, str]:
    """Validate essentials"""
    if "from manim import" not in code:
        return False, "Missing import"
    if "class DemoScene" not in code:
        return False, "Missing class"
    if "def construct" not in code:
        return False, "Missing method"
    return True, "Valid"