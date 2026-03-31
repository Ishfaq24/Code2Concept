from google import genai
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()

class LLMServiceManager:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash"
        self.max_retries = 3
        self.retry_delay = 1

    def retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry logic"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
                    print(f"⏳ Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ All {self.max_retries} attempts failed")
                    raise

    def generate_teaching_script(self, topic: str) -> dict:
        """Generate a comprehensive teaching script for any topic using Gemini"""
        prompt = f"""
        Create a detailed educational teaching script for the topic: "{topic}"
        
        Generate a structured JSON response with:
        {{
            "title": "The topic title",
            "description": "Brief description of what the topic is",
            "concept": "Core concept explanation",
            "steps": [
                "Step 1 with detailed explanation",
                "Step 2 with detailed explanation",
                "Step 3 with detailed explanation",
                "Step 4 with detailed explanation",
                "Step 5 with detailed explanation"
            ],
            "example": "A simple real-world example",
            "importance": "Why this concept matters",
            "duration_seconds": 90
        }}
        
        Make sure:
        - Each step is clear and educational
        - Include at least 5 steps
        - Add a real-world example
        - Duration should be 90-120 seconds for video
        - Return ONLY valid JSON, no markdown
        """
        
        def _call_gemini():
            res = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            text = res.text.strip()
            
            # Clean up markdown if present
            if text.startswith("```"):
                parts = text.split("```")
                if len(parts) >= 2:
                    text = parts[1].strip()
                if text.startswith("json"):
                    text = text[4:]
            
            return json.loads(text)
        
        try:
            script = self.retry_with_backoff(_call_gemini)
            print(f"✅ Teaching script generated for: {topic}")
            return script
        except Exception as e:
            print(f"❌ Script generation failed: {str(e)}")
            # Fallback to basic script
            return self._fallback_script(topic)

    def _fallback_script(self, topic: str) -> dict:
        """Fallback script generation when Gemini fails"""
        return {
            "title": topic.title(),
            "description": f"An introduction to {topic}",
            "concept": f"{topic} is a fundamental concept in computing",
            "steps": [
                f"{topic.title()} helps solve real-world problems",
                "Understanding the basics is essential",
                "It has practical applications",
                "Learning step by step builds expertise",
                "Practice and experimentation are key"
            ],
            "example": f"Consider this simple example of {topic}...",
            "importance": f"Mastering {topic} opens many opportunities",
            "duration_seconds": 90
        }

    def generate_manim_code(self, script: dict, enhancements: str = None) -> str:
        """Generate advanced Manim animation code from script using Gemini"""
        script_json = json.dumps(script, indent=2)
        
        prompt = f"""
        Generate beautiful, professional Manim animation code for this educational script:
        
        {script_json}
        
        Requirements:
        - Create a Scene class named "DemoScene"
        - Animate the title with Write animation
        - For each step, use different animations (Write, FadeIn, SlideIn, etc.)
        - Add transitions between steps with FadeOut/FadeIn
        - Include proper timing: ~{script.get('duration_seconds', 90)}ms per step
        - Add visual elements (shapes, colors, styling)
        - Make it engaging and educational
        - Include the example as a visual representation if possible
        - Use colors appropriately (Blue, Green, Yellow, etc.)
        - Ensure total video duration matches the duration_seconds specified
        
        Return ONLY valid Python code with:
        - Proper imports from manim
        - Single Scene class: class DemoScene(Scene)
        - Complete construct() method
        - No markdown, no comments with special chars
        - Code must be executable
        """
        
        if enhancements:
            prompt += f"\n\nAdditional requirements: {enhancements}"
        
        def _call_gemini():
            res = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            code = res.text.strip()
            
            # Clean up markdown
            if code.startswith("```"):
                parts = code.split("```")
                if len(parts) >= 2:
                    code = parts[1].strip()
                if code.startswith("python"):
                    code = code[6:]
            
            return code
        
        try:
            code = self.retry_with_backoff(_call_gemini)
            print("✅ Manim code generated successfully")
            return code
        except Exception as e:
            print(f"❌ Manim code generation failed: {str(e)}")
            return self._fallback_manim_code(script)

    def _fallback_manim_code(self, script: dict) -> str:
        """Fallback Manim code when generation fails"""
        title = script.get("title", "Topic")
        steps = script.get("steps", [])
        
        step_code = ""
        for i, step in enumerate(steps):
            step_code += f"""
        step{i} = Text("{step}").scale(0.5)
        step{i}.next_to(title, DOWN*{i+1})
        self.play(Write(step{i}))
        self.wait(1)
        """
        
        return f"""
from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("{title}").scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        {step_code}
        
        self.wait(2)
"""

# Singleton instance
_llm_service = None

def get_llm_service():
    """Get or create LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMServiceManager()
    return _llm_service

# Legacy function interfaces for backward compatibility
def generate_teaching_script(topic: str) -> dict:
    """Legacy interface - generates teaching script"""
    service = get_llm_service()
    return service.generate_teaching_script(topic)

def generate_manim_from_script(script: dict, enhancements: str = None) -> str:
    """Legacy interface - generates Manim code"""
    service = get_llm_service()
    return service.generate_manim_code(script, enhancements)