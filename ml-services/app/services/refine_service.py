"""
Refinement service for Manim code.
Currently uses simple feedback application instead of LLM refinement
to avoid hitting API rate limits.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def refine_code(code: str, attempt: int = 1) -> str:
    """
    Skip LLM refinement - generated code is pre-validated.
    
    Args:
        code: The Manim code to refine
        attempt: Current attempt number (unused, for compatibility)
        
    Returns:
        str: The same code (already validated)
    """
    print("⏭️  Refinement skipped (using pre-validated generated code)")
    return code


def get_refinement_feedback(code: str, user_feedback: str) -> str:
    """
    Apply user feedback to code using simple string modifications.
    Avoids LLM calls to prevent rate limiting.
    
    Args:
        code: Current Manim code
        user_feedback: User's requested changes
        
    Returns:
        str: Modified code based on feedback
    """
    
    print(f"✨ Applying user feedback: {user_feedback}")
    
    feedback_lower = user_feedback.lower()
    modified_code = code
    
    # Timing modifications
    if "slower" in feedback_lower or "slow" in feedback_lower:
        modified_code = modified_code.replace("run_time=0.8", "run_time=1.5")
        modified_code = modified_code.replace("run_time=1", "run_time=1.8")
        modified_code = modified_code.replace("run_time=1.2", "run_time=2")
        print("   ⏱️ Animations slowed down")
    
    if "faster" in feedback_lower or "speed" in feedback_lower:
        modified_code = modified_code.replace("run_time=2", "run_time=1")
        modified_code = modified_code.replace("run_time=1.8", "run_time=1.2")
        modified_code = modified_code.replace("run_time=1.5", "run_time=0.8")
        print("   ⚡ Animations sped up")
    
    # Color modifications
    if "dark" in feedback_lower or "darker" in feedback_lower:
        modified_code = modified_code.replace("#0a0a0a", "#000000")
        print("   🌑 Background darkened")
    
    if "bright" in feedback_lower or "lighter" in feedback_lower or "light" in feedback_lower:
        modified_code = modified_code.replace("#0a0a0a", "#1a1a1a")
        print("   ☀️ Background lightened")
    
    # Font size modifications
    if "larger" in feedback_lower or "bigger" in feedback_lower or "large text" in feedback_lower:
        modified_code = modified_code.replace("font_size=24,", "font_size=32,")
        modified_code = modified_code.replace("font_size=26,", "font_size=34,")
        modified_code = modified_code.replace("font_size=56,", "font_size=64,")
        print("   📝 Text size increased")
    
    if "smaller" in feedback_lower or "smaller text" in feedback_lower:
        modified_code = modified_code.replace("font_size=32,", "font_size=24,")
        modified_code = modified_code.replace("font_size=34,", "font_size=26,")
        modified_code = modified_code.replace("font_size=64,", "font_size=48,")
        print("   📝 Text size decreased")
    
    # Wait time modifications (affects overall pacing)
    if "longer" in feedback_lower or "longer pauses" in feedback_lower:
        modified_code = modified_code.replace("self.wait(1)", "self.wait(2)")
        modified_code = modified_code.replace("self.wait(1.8)", "self.wait(2.5)")
        print("   ⏸️ Pause durations increased")
    
    if "shorter" in feedback_lower or "faster paced" in feedback_lower:
        modified_code = modified_code.replace("self.wait(2)", "self.wait(1)")
        modified_code = modified_code.replace("self.wait(2.5)", "self.wait(1.5)")
        print("   ⏩ Pause durations decreased")
    
    if modified_code != code:
        print("✅ Feedback applied successfully")
    else:
        print("ℹ️ No recognized feedback patterns applied")
    
    return modified_code