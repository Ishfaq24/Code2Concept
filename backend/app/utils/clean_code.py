"""
Code cleaning and validation utilities for generated Manim code.
Ensures all imports are present and syntax is valid.
"""


def clean_code(code: str) -> str:
    """
    Clean and validate generated Manim code.
    
    Operations:
    - Remove markdown wrapping (```, ```python)
    - Ensure manim imports are present
    - Fix common syntax issues
    - Remove stray comments/quotes
    
    Args:
        code: Raw generated Manim code
        
    Returns:
        str: Clean, validated Manim code
    """
    
    # Remove markdown wrapping
    code = code.replace("```python", "").replace("```", "").strip()
    
    # Ensure imports are at the beginning
    if "from manim import" not in code:
        # Add imports at the beginning
        code = "from manim import *\n\n" + code
        print("   ℹ️ Added missing Manim import")
    
    # Ensure imports are on first line
    lines = code.split('\n')
    
    # Find import line
    import_line_idx = None
    for i, line in enumerate(lines):
        if "from manim import" in line:
            import_line_idx = i
            break
    
    # Move import to top if not already
    if import_line_idx is not None and import_line_idx > 0:
        import_line = lines.pop(import_line_idx)
        lines.insert(0, import_line)
        print("   ℹ️ Moved import statement to top")
    
    code = '\n'.join(lines)
    
    # Remove stray docstrings or comments that might cause issues
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that are only docstring markers without content
        if '"""' in line or "'''" in line:
            # Keep docstrings only if they're part of class/function definition
            if 'def ' in line or 'class ' in line:
                cleaned_lines.append(line)
            continue
        
        cleaned_lines.append(line)
    
    code = '\n'.join(cleaned_lines)
    
    # Fix common color issues (ensure colors are used correctly)
    # Replace color=CYAN, with proper syntax
    code = code.replace("color = CYAN", "color=CYAN")
    code = code.replace("color = RED", "color=RED")
    code = code.replace("color = BLUE", "color=BLUE")
    code = code.replace("color = GREEN", "color=GREEN")
    code = code.replace("color = YELLOW", "color=YELLOW")
    code = code.replace("color = PURPLE", "color=PURPLE")
    code = code.replace("color = ORANGE", "color=ORANGE")
    code = code.replace("color = WHITE", "color=WHITE")
    code = code.replace("color = GREY_B", "color=GREY_B")
    code = code.replace("color = BLACK", "color=BLACK")
    
    # Fix weight parameter
    code = code.replace("weight = BOLD", "weight=BOLD")
    
    # Remove trailing whitespace from each line
    lines = code.split('\n')
    lines = [line.rstrip() for line in lines]
    code = '\n'.join(lines)
    
    # Remove multiple consecutive blank lines (keep max 2)
    while '\n\n\n' in code:
        code = code.replace('\n\n\n', '\n\n')
    
    return code.strip()


def validate_manim_code(code: str) -> tuple[bool, str]:
    """
    Validate generated Manim code for basic correctness.
    
    Args:
        code: Manim code to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    
    # Check for required imports
    if "from manim import" not in code:
        return False, "Missing 'from manim import *' statement"
    
    # Check for class definition
    if "class DemoScene" not in code:
        return False, "Missing 'class DemoScene(Scene):' definition"
    
    # Check for construct method
    if "def construct" not in code:
        return False, "Missing 'def construct(self):' method"
    
    # Check for basic structure
    if "self.play" not in code:
        return False, "No animations (self.play) found in code"
    
    # Check indentation isn't completely broken
    lines = code.split('\n')
    in_class = False
    in_method = False
    
    for i, line in enumerate(lines):
        if "class DemoScene" in line:
            in_class = True
            continue
        
        if in_class and "def construct" in line:
            in_method = True
            # Should be indented
            if not line.startswith(" "):
                return False, f"Method definition not properly indented (line {i})"
            continue
        
        if in_method and line.strip() and not line.startswith(" "):
            if not line.startswith("class") and not line.startswith("def"):
                # Code inside method should be indented
                if "self." in line:
                    return False, f"Method body not properly indented (line {i})"
    
    return True, "Code validation passed"