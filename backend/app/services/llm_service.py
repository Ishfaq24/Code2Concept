import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMServiceManager:
    """Generates complete Manim code with embedded script in one call"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "google/gemma-4-31b-it"
        
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found")
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        print(f"✅ LLM Service initialized")

    def generate_manim_video_code(self, topic: str) -> str:
        """Generate COMPLETE Manim code in ONE call - no separate steps"""
        
        prompt = f"""Generate COMPLETE Manim animation code for: {topic}

CRITICAL RULES - FOLLOW EXACTLY:
1. Start with: from manim import *
2. Class MUST be named: class DemoScene(Scene):
3. Method MUST be named: def construct(self):
4. Every single line MUST be complete on ONE line - NO line breaks in function calls
5. Use only colors: BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, WHITE, GREY_B
6. NO undefined variables
7. NO special characters that break Python
8. Return ONLY executable code - NO markdown, NO explanations, NO comments
9. Make animations educational about {topic}
10. Total duration should be around 2 minutes

Example format (FOLLOW THIS EXACTLY):
from manim import *

class DemoScene(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        title = Text("Binary Search", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        line = Line(LEFT*2.5, RIGHT*2.5, color=BLUE, stroke_width=2)
        line.next_to(title, DOWN*0.3)
        self.play(Create(line), run_time=0.8)
        self.wait(0.5)
        concept = Text("Efficiently search sorted arrays", font_size=18, color=GREY_B)
        concept.next_to(line, DOWN*0.8)
        self.play(FadeIn(concept), run_time=0.8)
        self.wait(1)
        step1 = Text("Step 1: Start with sorted data", font_size=16, color=RED)
        step1.next_to(concept, DOWN*1.5)
        self.play(FadeIn(step1), run_time=0.8)
        self.wait(1)
        step2 = Text("Step 2: Pick middle element", font_size=16, color=BLUE)
        step2.next_to(step1, DOWN*0.8)
        self.play(FadeIn(step2), run_time=0.8)
        self.wait(1)
        step3 = Text("Step 3: Eliminate half the data", font_size=16, color=GREEN)
        step3.next_to(step2, DOWN*0.8)
        self.play(FadeIn(step3), run_time=0.8)
        self.wait(1)
        step4 = Text("Step 4: Repeat until found", font_size=16, color=YELLOW)
        step4.next_to(step3, DOWN*0.8)
        self.play(FadeIn(step4), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(line), FadeOut(concept), FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(step4), run_time=1.5)
        self.wait(0.5)

Now generate complete working code for teaching {topic}:"""
        
        try:
            print(f"🎬 Generating Manim video code for: {topic}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=1500
            )
            
            code = response.choices[0].message.content.strip()
            
            print("\n" + "="*80)
            print("📝 RAW CODE FROM API:")
            print("="*80)
            print(code[:800])
            print("\n..." if len(code) > 800 else "")
            print("="*80 + "\n")
            
            # Clean markdown
            if code.startswith("```python"):
                code = code[9:]
            elif code.startswith("```"):
                code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
            
            code = code.strip()
            
            # ENSURE IMPORT IS FIRST
            lines = code.split('\n')
            import_line = None
            other_lines = []
            
            for line in lines:
                if "from manim import" in line:
                    import_line = line
                else:
                    other_lines.append(line)
            
            if not import_line:
                import_line = "from manim import *"
            
            code = import_line + "\n" + "\n".join(other_lines)
            
            # ENSURE CLASS NAME IS DemoScene
            import re
            code = re.sub(r'class \w+Scene\(Scene\):', 'class DemoScene(Scene):', code)
            
            # JOIN INCOMPLETE LINES
            lines = code.split('\n')
            fixed = []
            i = 0
            while i < len(lines):
                line = lines[i].rstrip()
                while i < len(lines) - 1 and (line.endswith(',') or line.endswith('(')):
                    i += 1
                    line = line + ' ' + lines[i].lstrip()
                fixed.append(line)
                i += 1
            
            code = '\n'.join(fixed)
            
            print("="*80)
            print("✅ CLEANED CODE (first 20 lines):")
            print("="*80)
            print_lines = code.split('\n')[:20]
            for i, line in enumerate(print_lines, 1):
                print(f"{i}: {line}")
            print("="*80 + "\n")
            
            return code
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._fallback_code(topic)

    def _fallback_code(self, topic: str) -> str:
        """Fallback code - GUARANTEED TO WORK"""
        return f"""from manim import *

class DemoScene(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        title = Text('{topic}', font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        line = Line(LEFT*2.5, RIGHT*2.5, color=BLUE, stroke_width=2)
        line.next_to(title, DOWN*0.3)
        self.play(Create(line), run_time=0.8)
        self.wait(0.5)
        concept = Text('Understanding the fundamentals', font_size=18, color=GREY_B)
        concept.next_to(line, DOWN*0.8)
        self.play(FadeIn(concept), run_time=0.8)
        self.wait(1)
        step1 = Text('Step 1: Learn the basics', font_size=16, color=RED)
        step1.next_to(concept, DOWN*1.5)
        self.play(FadeIn(step1), run_time=0.8)
        self.wait(1)
        step2 = Text('Step 2: Understand applications', font_size=16, color=BLUE)
        step2.next_to(step1, DOWN*0.8)
        self.play(FadeIn(step2), run_time=0.8)
        self.wait(1)
        step3 = Text('Step 3: Practice implementation', font_size=16, color=GREEN)
        step3.next_to(step2, DOWN*0.8)
        self.play(FadeIn(step3), run_time=0.8)
        self.wait(1)
        step4 = Text('Step 4: Master the concept', font_size=16, color=YELLOW)
        step4.next_to(step3, DOWN*0.8)
        self.play(FadeIn(step4), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(line), FadeOut(concept), FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(step4), run_time=1.5)
        self.wait(0.5)
"""

    def generate_teaching_script(self, topic: str) -> dict:
        """Deprecated - kept for compatibility"""
        return {"title": topic.title(), "concept": topic}


_llm_service = None

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMServiceManager()
    return _llm_service

def generate_teaching_script(topic: str) -> dict:
    return get_llm_service().generate_teaching_script(topic)

def generate_manim_from_script(script: dict) -> str:
    """For backward compatibility"""
    return get_llm_service().generate_manim_video_code(script.get("title", "Topic"))