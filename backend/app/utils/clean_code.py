import re


def clean_code(code: str) -> str:
    """Minimal cleaning and small compatibility fixes"""
    # Strip possible markdown fences
    code = code.replace("```python", "").replace("```", "").strip()

    # Manim Community v0.20.1 does not define the CYAN constant.
    # Replace bare CYAN usage with an explicit hex color so generated
    # code doesn't crash at runtime with NameError.
    code = re.sub(r"\bCYAN\b", '"#00FFFF"', code)

    # Some generations incorrectly pass SurroundingRectangle directly into
    # self.play, which Manim does not accept. Rewrite simple one-line usages
    # into a variable + Create() animation so they run correctly.
    code = re.sub(
        r"(^\s*)self\.play\(\s*SurroundingRectangle\((.+)\)\s*\)",
        r"\1highlight_box = SurroundingRectangle(\2)\n\1self.play(Create(highlight_box))",
        code,
        flags=re.MULTILINE,
    )

    # Ensure numpy is available when generated code uses np.* helpers
    if "np." in code and "import numpy as np" not in code:
        if "from manim import *" in code:
            code = code.replace(
                "from manim import *",
                "from manim import *\nimport numpy as np",
                1,
            )
        else:
            code = "import numpy as np\n" + code

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