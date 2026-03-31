import ast
import re
from typing import Tuple

class CodeValidator:
    """Validates generated Manim code before rendering"""
    
    @staticmethod
    def validate_syntax(code: str) -> Tuple[bool, str]:
        """
        Check if code has valid Python syntax
        Returns: (is_valid, error_message)
        """
        try:
            ast.parse(code)
            return True, "✅ Syntax is valid"
        except SyntaxError as e:
            error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
            return False, error_msg
        except Exception as e:
            return False, f"Parse Error: {str(e)}"

    @staticmethod
    def validate_scene_class(code: str) -> Tuple[bool, str]:
        """
        Check if code contains DemoScene class with construct method
        """
        if "class DemoScene" not in code:
            return False, "❌ Missing 'class DemoScene' definition"
        
        if "def construct(self):" not in code:
            return False, "❌ Missing 'def construct(self):' method"
        
        return True, "✅ Scene class structure is valid"

    @staticmethod
    def validate_manim_imports(code: str) -> Tuple[bool, str]:
        """
        Check if code has required Manim imports
        """
        if "from manim import" not in code and "import manim" not in code:
            return False, "❌ Missing Manim imports"
        
        return True, "✅ Manim imports are present"

    @staticmethod
    def validate_animations(code: str) -> Tuple[bool, str]:
        """
        Check if code uses animations (self.play)
        """
        if "self.play(" not in code:
            return False, "⚠️ No animations found (self.play calls)"
        
        return True, "✅ Animations are present"

    @staticmethod
    def check_common_issues(code: str) -> list:
        """
        Check for common issues in Manim code
        Returns list of warnings
        """
        warnings = []
        
        # Check for markdown code fences
        if "```" in code:
            warnings.append("⚠️ Warning: Code contains markdown fences (```)")
        
        # Check for undefined variables
        undefined_patterns = [
            r"DOWN\s*\*\s*\d+(?!\s*\))",  # Incorrect DOWN usage
        ]
        
        # Check for very short code
        lines = code.strip().split('\n')
        if len(lines) < 10:
            warnings.append("⚠️ Warning: Code is very short, may lack content")
        
        return warnings

    @staticmethod
    def full_validation(code: str) -> dict:
        """
        Run all validations and return comprehensive report
        """
        report = {
            "is_valid": False,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        # Syntax check
        valid, msg = CodeValidator.validate_syntax(code)
        report["checks"]["syntax"] = msg
        if not valid:
            report["errors"].append(msg)
            return report  # Stop if syntax is invalid
        
        # Scene class check
        valid, msg = CodeValidator.validate_scene_class(code)
        report["checks"]["scene_class"] = msg
        if not valid:
            report["errors"].append(msg)
        
        # Imports check
        valid, msg = CodeValidator.validate_manim_imports(code)
        report["checks"]["imports"] = msg
        if not valid:
            report["errors"].append(msg)
        
        # Animations check
        valid, msg = CodeValidator.validate_animations(code)
        report["checks"]["animations"] = msg
        if not valid:
            report["warnings"].append(msg)
        
        # Common issues check
        issues = CodeValidator.check_common_issues(code)
        report["warnings"].extend(issues)
        
        # Overall validation
        report["is_valid"] = len(report["errors"]) == 0
        
        return report

def validate_manim_code(code: str) -> dict:
    """Main validation function"""
    return CodeValidator.full_validation(code)