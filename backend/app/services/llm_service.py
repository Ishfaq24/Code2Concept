import os
import json
import re
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMServiceManager:
    """Manages LLM interactions using NVIDIA API"""
    
    def __init__(self):
        """Initialize NVIDIA API client"""
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "google/gemma-4-31b-it"
        
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in .env")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        print(f"✅ LLM Service initialized with NVIDIA API")
        print(f"   Model: {self.model}")
        print(f"   Base URL: {self.base_url}")

    def generate_teaching_script(self, topic: str) -> dict:
        """
        Generate comprehensive teaching script using NVIDIA API
        
        Args:
            topic: The educational topic to create content for
            
        Returns:
            dict: Script with title, concept, steps, example, and duration
        """
        
        prompt = f"""You are an expert educational content creator. Create a detailed teaching script for: "{topic}"

Return ONLY valid JSON (no markdown, no extra text):
{{
    "title": "Clear, concise topic title",
    "concept": "1-2 sentence explanation of the core concept",
    "steps": [
        "Step 1: Detailed explanation with context",
        "Step 2: Detailed explanation with context",
        "Step 3: Detailed explanation with context",
        "Step 4: Detailed explanation with context",
        "Step 5: Detailed explanation with context",
        "Step 6: Detailed explanation with context"
    ],
    "example": "A clear, practical real-world example",
    "importance": "Why this concept matters in 1-2 sentences",
    "duration_seconds": 120
}}

Requirements:
- Minimum 6 steps (can have more for longer topics)
- Each step should be educational and build on previous ones
- Include practical examples where applicable
- Make the content engaging for learners
- Return ONLY the JSON object, nothing else
- Ensure all steps are relevant to the topic"""
        
        try:
            print("🤖 Calling NVIDIA API for script generation...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500,
                top_p=0.9
            )
            
            text = response.choices[0].message.content.strip()
            
            # Extract JSON from potential markdown wrapping
            if "```" in text:
                parts = text.split("```")
                for part in parts:
                    if part.startswith("json"):
                        text = part[4:].strip()
                        break
                    elif "{" in part:
                        text = part.strip()
                        break
            
            # Parse JSON
            parsed = json.loads(text)
            
            # Validate required fields
            required_fields = ["title", "concept", "steps"]
            for field in required_fields:
                if field not in parsed or not parsed[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure steps is a list with at least 6 items
            if not isinstance(parsed["steps"], list):
                raise ValueError("Steps must be a list")
            
            if len(parsed["steps"]) < 6:
                # Add more steps if needed
                while len(parsed["steps"]) < 6:
                    parsed["steps"].append(f"Additional point about {topic}")
            
            # Set default duration if missing
            if "duration_seconds" not in parsed:
                parsed["duration_seconds"] = 120
            
            print(f"✅ Teaching script generated: {parsed.get('title')}")
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            print(f"   Response text: {text[:200]}...")
            return self._fallback_script(topic)
        except Exception as e:
            print(f"❌ Script generation error: {e}")
            return self._fallback_script(topic)

    def _fallback_script(self, topic: str) -> dict:
        """
        Fallback script when API fails
        
        Args:
            topic: The topic for fallback content
            
        Returns:
            dict: Basic script structure
        """
        return {
            "title": topic.title(),
            "concept": f"{topic} is a fundamental concept that helps us understand and solve problems effectively.",
            "steps": [
                f"Understanding {topic.title()}: Definition and basic concepts",
                "The core principles and foundations behind this concept",
                "How it works in real-world scenarios and applications",
                "Practical applications and use cases in industry",
                "Key advantages, benefits, and why it matters",
                "Getting started and next steps for learning more"
            ],
            "example": f"For example, consider how {topic} is used in practical scenarios and everyday life to solve problems.",
            "importance": f"Mastering {topic} opens doors to better problem-solving and career opportunities.",
            "duration_seconds": 120
        }

    def generate_manim_code(self, script: dict) -> str:
        """
        Generate beautiful, valid Manim animation code
        
        Args:
            script: dict with title, concept, steps, example
            
        Returns:
            str: Valid, executable Manim Python code
        """
        
        title = script.get("title", "Topic")
        concept = script.get("concept", "")
        steps = script.get("steps", [])
        example = script.get("example", "")
        
        # Format steps for prompt
        steps_list = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        prompt = f"""You are an expert Manim animation developer. Generate ONLY professional, beautiful Manim code. NO explanations.

TOPIC: {title}
CONCEPT: {concept}

STEPS TO ANIMATE:
{steps_list}

EXAMPLE: {example}

CRITICAL REQUIREMENTS:
1. Start with: from manim import *
2. Create class DemoScene(Scene):
3. Use def construct(self): method
4. Use ONLY these valid colors: CYAN, RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, WHITE, GREY_B, BLACK, GRAY
5. Proper 4-space indentation
6. NO undefined variables
7. Use animations: Write, FadeIn, GrowFromCenter, Create, Transform, SlideIn
8. Add self.wait() between animations (1-2 seconds)
9. Total video duration: ~2 minutes (adjust wait times accordingly)
10. Professional dark background: self.camera.background_color = "#0a0a0a"
11. NO special characters in strings that could break Python
12. Escape any quotes properly in Text() fields
13. Return ONLY valid, executable Python code
14. No markdown backticks, no comments, no docstrings

STRUCTURE EXAMPLE:
from manim import *

class DemoScene(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        title = Text("Title", font_size=56, color=CYAN, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        line = Line(title.get_left() - RIGHT * 0.5, title.get_right() + RIGHT * 0.5, color=CYAN, stroke_width=2)
        self.play(Create(line), run_time=1)
        self.wait(0.5)
        
        concept_text = Text("Core Concept", font_size=26, color=GREY_B)
        concept_text.next_to(line, DOWN * 1.2)
        self.play(FadeIn(concept_text, shift=UP), run_time=1)
        self.wait(1)
        
        step_1 = Text("Step 1 content", font_size=24, color=RED)
        step_1.next_to(concept_text, DOWN * 2)
        self.play(FadeIn(step_1, shift=DOWN), run_time=1.2)
        self.wait(1.5)
        
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(line), FadeOut(concept_text), run_time=1.5)
        self.wait(0.5)

Generate complete production-ready code now:"""
        
        try:
            print("🎨 Calling NVIDIA API for Manim code generation...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.65,
                max_tokens=3500,
                top_p=0.95
            )
            
            code = response.choices[0].message.content.strip()
            
            # Clean markdown wrapping
            if code.startswith("```python"):
                code = code[9:]
            elif code.startswith("```"):
                code = code[3:]
            
            if code.endswith("```"):
                code = code[:-3]
            
            code = code.strip()
            
            # Validate code structure
            if "class DemoScene" not in code:
                print("⚠️ Generated code missing DemoScene class, adding fallback")
                return self._fallback_manim_code(script)
            
            if "def construct" not in code:
                print("⚠️ Generated code missing construct method, adding fallback")
                return self._fallback_manim_code(script)
            
            if "from manim import" not in code:
                print("⚠️ Missing imports, adding them...")
                code = "from manim import *\n\n" + code
            
            # Fix common issues
            code = self._fix_code_issues(code)
            
            print("✅ Manim code generated successfully")
            return code
                
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
            return self._fallback_manim_code(script)

    def _fix_code_issues(self, code: str) -> str:
        """
        Fix common issues in generated code
        
        Args:
            code: Generated Manim code
            
        Returns:
            str: Fixed code
        """
        # Fix quote issues
        code = code.replace('""', '"')
        
        # Ensure proper spacing around = in parameters
        code = code.replace("= CYAN", "=CYAN")
        code = code.replace("= RED", "=RED")
        code = code.replace("= BLUE", "=BLUE")
        code = code.replace("= GREEN", "=GREEN")
        code = code.replace("= YELLOW", "=YELLOW")
        code = code.replace("= PURPLE", "=PURPLE")
        code = code.replace("= ORANGE", "=ORANGE")
        code = code.replace("= WHITE", "=WHITE")
        code = code.replace("= GREY_B", "=GREY_B")
        code = code.replace("= BLACK", "=BLACK")
        code = code.replace("= BOLD", "=BOLD")
        
        return code

    def _fallback_manim_code(self, script: dict) -> str:
        """
        Fallback Manim code when generation fails
        
        Args:
            script: dict with title, concept, steps
            
        Returns:
            str: Valid Manim code
        """
        title = script.get("title", "Topic")
        concept = script.get("concept", "")
        steps = script.get("steps", [])
        
        colors = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE", "CYAN", "WHITE"]
        
        step_animations = ""
        for i, step in enumerate(steps):
            color = colors[i % len(colors)]
            step_text = step[:60] if len(step) > 60 else step
            # Escape quotes in step text
            step_text = step_text.replace('"', "'")
            step_animations += f"""
        # Step {i+1}
        step_{i}_text = Text("{step_text}", font_size=24, color={color})
        step_{i}_text.next_to(concept_display, DOWN * {i+2.2})
        self.play(FadeIn(step_{i}_text, shift=DOWN), run_time=1.2)
        self.wait(1.8)
"""
        
        # Escape quotes in title and concept
        title_escaped = title.replace('"', "'")
        concept_escaped = concept.replace('"', "'")
        
        return f"""from manim import *

class DemoScene(Scene):
    def construct(self):
        # Setup
        self.camera.background_color = "#0a0a0a"
        
        # Title animation
        title = Text("{title_escaped}", font_size=56, color=CYAN, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(0.5)
        
        # Underline
        line = Line(
            title.get_left() - RIGHT * 0.5,
            title.get_right() + RIGHT * 0.5,
            color=CYAN,
            stroke_width=2
        )
        self.play(Create(line), run_time=1)
        self.wait(0.5)
        
        # Concept display
        concept_display = Text("{concept_escaped}", font_size=26, color=GREY_B)
        concept_display.next_to(line, DOWN * 1.2)
        self.play(FadeIn(concept_display, shift=UP), run_time=1)
        self.wait(1)
        
        # Step animations
{step_animations}
        
        # Closing animation
        self.wait(1.5)
        self.play(
            FadeOut(title),
            FadeOut(line),
            FadeOut(concept_display),
            run_time=1.5
        )
        self.wait(0.5)
"""


# Singleton instance
_llm_service = None


def get_llm_service() -> LLMServiceManager:
    """Get or create LLM service instance (singleton pattern)"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMServiceManager()
    return _llm_service


# Legacy function interfaces for backward compatibility
def generate_teaching_script(topic: str) -> dict:
    """Generate teaching script for a topic"""
    service = get_llm_service()
    return service.generate_teaching_script(topic)


def generate_manim_from_script(script: dict) -> str:
    """Generate Manim code from a teaching script"""
    service = get_llm_service()
    return service.generate_manim_code(script)