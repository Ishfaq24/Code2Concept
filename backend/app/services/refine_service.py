from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def refine_code(code: str, attempt: int = 1) -> str:
    """Refine Manim code with multiple retry attempts"""
    
    if attempt > 3:
        print("❌ Max refinement attempts reached")
        return code
    
    prompt = f"""
    Fix this Manim code for errors. IMPORTANT:
    
    - Fix ANY syntax errors
    - Ensure all imports are correct
    - Fix undefined variables
    - Keep the animations beautiful
    - Do NOT add new features
    
    Return ONLY Python code, no markdown.
    
    CODE:
    {code}
    """
    
    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        refined_code = res.text.strip()
        
        if refined_code.startswith("```"):
            refined_code = refined_code.split("```")[1]
            if refined_code.startswith("python"):
                refined_code = refined_code[6:]
            refined_code = refined_code.split("```")[0]
        
        refined_code = refined_code.strip()
        
        print(f"✅ Code refined (Attempt {attempt}/3)")
        return refined_code
        
    except Exception as e:
        print(f"⚠️ Refinement attempt {attempt} failed: {e}")
        if attempt < 3:
            print(f"🔄 Retrying...")
            return refine_code(code, attempt + 1)
        return code


def get_refinement_feedback(code: str, user_feedback: str) -> str:
    """Apply user feedback to refine code"""
    
    prompt = f"""
    Apply these user changes to the Manim code:
    
    USER REQUEST: {user_feedback}
    
    Current code:
    {code}
    
    Return ONLY updated Python code, no markdown.
    """
    
    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        updated_code = res.text.strip()
        
        if updated_code.startswith("```"):
            updated_code = updated_code.split("```")[1]
            if updated_code.startswith("python"):
                updated_code = updated_code[6:]
            updated_code = updated_code.split("```")[0]
        
        print("✅ User feedback applied")
        return updated_code
        
    except Exception as e:
        print(f"❌ Failed to apply feedback: {e}")
        return code