import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMServiceManager:
    """Generates high-quality Manim animation code with visual storytelling"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "google/gemma-4-31b-it"

        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        print("✅ LLM Service initialized")

    def generate_manim_video_code(self, topic: str) -> str:
        """Generate COMPLETE Manim code with strong visual storytelling"""

        prompt = f"""
Generate COMPLETE Manim animation code for: {topic}

CRITICAL SETUP RULES:
1. Start with: from manim import *
2. Class MUST be named: class DemoScene(Scene):
3. Method MUST be named: def construct(self):
4. Return ONLY executable Python code (NO markdown, NO explanations, NO comments)
5. Code MUST run without errors. NO undefined variables.
6. When highlighting with SurroundingRectangle, first assign it to a variable 
   (e.g. box = SurroundingRectangle(target, color=YELLOW)) and then call self.play(Create(box)).

LAYOUT & POSITIONING (HOW TO AVOID OVERLAPPING & OUT-OF-BOUNDS):
1. NEVER leave elements at the default center origin if multiple elements exist. 
2. STRICT RELATIVE POSITIONING: Always position new elements relative to existing ones using `.next_to(previous_element, DOWN, buff=0.5)`.
3. PREVENT OUT OF BOUNDS: Maximum `font_size` for Titles is 40. Maximum `font_size` for body text is 28.
4. SHORT TEXT ONLY: Never write long paragraphs. Break long sentences into multiple small Text objects or use VGroup to stack short sentences.
5. VGROUP ARRANGEMENT: If showing a list, put them in a `VGroup` and use `group.arrange(DOWN, aligned_edge=LEFT, buff=0.4)`.

SCENE MANAGEMENT & ORDERED RENDERING:
1. CLEAR THE SCREEN: To prevent overcrowding and overlaps, you MUST clear the screen between major concepts using: `self.play(FadeOut(*self.mobjects))`
2. STRICT SEQUENCE: Animate step-by-step. 
   - Define Element A -> Position it -> self.play(Write(A)) -> self.wait(1)
   - Define Element B -> Position relative to A -> self.play(FadeIn(B)) -> self.wait(1)
3. Do not define all elements at the top. Define, position, and animate them chronologically.

VIDEO QUALITY & STORYTELLING:
1. STRUCTURE: Title Introduction -> Clear Screen -> Visual Breakdown -> Clear Screen -> Final Summary.
2. VISUALS: Use arrows (`Arrow`), boxes (`SurroundingRectangle`), and shapes (`Circle`, `Rectangle`) to illustrate concepts rather than just text.
3. PACING: Always include `self.wait(1)` or `self.wait(2)` after every animation.

Now generate clean, sequentially ordered, properly spaced animation code for: {topic}
"""

        try:
            print(f"🎬 Generating Manim video code for: {topic}")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )

            code = response.choices[0].message.content.strip()

            print("\n" + "=" * 80)
            print("📝 RAW CODE FROM API:")
            print("=" * 80)
            print(code[:800])
            print("\n..." if len(code) > 800 else "")
            print("=" * 80 + "\n")

            # 🔧 CLEAN MARKDOWN
            code = self._clean_markdown(code)

            # 🔧 ENSURE IMPORT
            code = self._ensure_import(code)

            # 🔧 ENSURE CLASS NAME
            code = self._fix_class_name(code)

            # 🔧 FINAL SANITY CLEAN
            code = self._final_cleanup(code)

            print("=" * 80)
            print("✅ CLEANED CODE (first 25 lines):")
            print("=" * 80)
            for i, line in enumerate(code.split("\n")[:25], 1):
                print(f"{i}: {line}")
            print("=" * 80 + "\n")

            return code

        except Exception as e:
            print(f"❌ Error: {e}")
            return self._fallback_code(topic)

    def generate_narration_text(
        self,
        topic: str,
        language_name: str = "English",
        language_code: str = "en",
    ) -> str:
        """Generate a spoken narration script for the given topic.

        The script is plain text, suitable to be read aloud by TTS.
        """

        prompt = f"""
You are an expert educator and voice-over writer.

Write a clear, engaging narration script for an educational video
about the topic: "{topic}".
Write the entire narration in {language_name}.
If language is Hindi, you MUST write in Devanagari script.

Constraints:
- Plain text only (no markdown, no bullet points, no headings).
- 6-12 short sentences, conversational and student-friendly.
- Explain step by step, as if speaking in a video.
- Do not include scene directions or camera cues.
- Do not mention that you are an AI.
"""

        try:
            print(f"🗣️ Generating narration script for: {topic} ({language_name}/{language_code})")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=700,
            )

            narration = response.choices[0].message.content.strip()

            # Remove any stray markdown fences just in case
            if narration.startswith("```"):
                narration = narration.split("\n", 1)[-1]
            if narration.endswith("```"):
                narration = narration.rsplit("\n", 1)[0]

            narration = self._ensure_target_language(
                text=narration,
                topic=topic,
                language_name=language_name,
                language_code=language_code,
            )

            print("✅ Narration script generated")
            return narration

        except Exception as e:
            print(f"❌ Error generating narration script: {e}")
            # Fallback to language-aware generic narration
            if language_code == "hi":
                return (
                    f"इस पाठ में हम {topic} के मुख्य विचारों को सरल तरीके से समझेंगे। "
                    "सबसे पहले हम इसकी मूल अवधारणा देखेंगे। "
                    "फिर एक आसान उदाहरण के साथ इसे समझेंगे। "
                    "अंत में हम जानेंगे कि इसे वास्तविक जीवन में कैसे उपयोग किया जाता है।"
                )
            return (
                f"In this lesson, we will quickly explore the core ideas of {topic}. "
                "We will start with the basic intuition, then walk through a simple example, "
                "and finally connect the concept back to real-world usage."
            )

    def generate_study_guide(
        self,
        topic: str,
        language_name: str = "English",
        language_code: str = "en",
    ) -> dict:
        """Generate a richer study guide that can be exported as a PDF."""

        prompt = f"""
You are an expert teacher writing a polished study guide for a PDF handout.

Create a detailed, classroom-ready study guide about the topic: "{topic}".
Write the entire response in English only.
Do not use any non-English script, even if the video narration is in another language.

Return ONLY valid JSON with this structure:
{{
  "title": "...",
  "subtitle": "...",
  "overview": "...",
  "core_concepts": [
    {{"heading": "...", "content": "..."}},
    {{"heading": "...", "content": "..."}}
  ],
  "worked_example": "...",
  "real_world_applications": ["...", "...", "..."],
  "common_misconceptions": ["...", "...", "..."],
  "quick_recap": "...",
  "practice_questions": ["...", "...", "..."],
  "further_learning": ["...", "...", "..."]
}}

Rules:
- No markdown fences, no commentary, no extra keys.
- Make the content substantial enough for a 3-5 page PDF.
- Use plain, precise language with strong conceptual explanations.
- Include intuition, step-by-step logic, a worked example, common mistakes, and revision questions.
- Avoid fluff; every section should add learning value.
- Keep each paragraph reasonably short so it fits nicely in a printed handout.
"""

        try:
            print(f"📘 Generating study guide for: {topic} ({language_name}/{language_code})")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=2200,
            )

            raw_text = response.choices[0].message.content.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.split("\n", 1)[-1]
            if raw_text.endswith("```"):
                raw_text = raw_text.rsplit("\n", 1)[0]

            guide = json.loads(raw_text)
            guide["title"] = guide.get("title") or f"Study Guide: {topic}"
            guide["subtitle"] = guide.get("subtitle") or "A detailed revision guide for study and review"
            guide["overview"] = guide.get("overview") or ""
            guide["core_concepts"] = guide.get("core_concepts") or []
            guide["worked_example"] = guide.get("worked_example") or ""
            guide["real_world_applications"] = guide.get("real_world_applications") or []
            guide["common_misconceptions"] = guide.get("common_misconceptions") or []
            guide["quick_recap"] = guide.get("quick_recap") or ""
            guide["practice_questions"] = guide.get("practice_questions") or []
            guide["further_learning"] = guide.get("further_learning") or []

            return guide

        except Exception as e:
            print(f"❌ Error generating study guide: {e}")
            return self._fallback_study_guide(topic, language_name, language_code)

    def _fallback_study_guide(self, topic: str, language_name: str, language_code: str) -> dict:
        return {
            "title": f"Study Guide: {topic}",
            "subtitle": "A detailed revision handout for learning and review",
            "overview": f"This guide explains the core ideas of {topic}, how it works, and why it matters in practical settings. The goal is to give you a clear, printable reference you can read before revision or use after watching the video.",
            "core_concepts": [
                {"heading": "Core Idea", "content": f"Start by understanding the main purpose and intuition behind {topic}. Ask what problem it solves and why that problem is important."},
                {"heading": "How It Works", "content": "Break the topic into small steps so the process becomes easier to follow and remember. When the steps are clear, the entire concept becomes much easier to retain."},
                {"heading": "Why It Matters", "content": "This concept is useful because it helps with reasoning, problem-solving, and real-world applications. It is not just theory; it is a method for thinking and making predictions."},
                {"heading": "Key Terms to Remember", "content": "Keep track of the main vocabulary, because strong definitions make revision easier and help you explain the topic with confidence."},
            ],
            "worked_example": f"A simple example helps connect theory to practice. For {topic}, imagine applying the idea step by step in a real scenario. Begin by identifying the input, then follow the process, and finally check the result against the expected outcome.",
            "real_world_applications": [
                f"Learning and teaching {topic} more effectively",
                f"Using {topic} to solve practical problems",
                "Connecting the concept to everyday decisions and analysis",
                "Building more advanced ideas on top of the same foundation",
            ],
            "common_misconceptions": [
                "It is often more approachable than it first appears when broken into steps.",
                "Memorizing definitions is not enough without understanding the intuition.",
                "Examples are essential for long-term recall and confidence.",
                "A concept that seems simple can still be misunderstood if the process is not practiced.",
            ],
            "quick_recap": f"In short, {topic} becomes much easier to master when you study its definition, process, examples, and applications together. Review the core idea, test yourself with the example, and then revisit the misconceptions to see if you can explain the topic clearly.",
            "practice_questions": [
                f"Explain {topic} in your own words.",
                f"Give one real-world example of {topic}.",
                f"Which part of {topic} is most important and why?",
                "What mistake would a beginner most likely make when first learning this topic?",
            ],
            "further_learning": [
                "Draw a simple diagram to revise the concept.",
                "Teach the topic to a friend in two minutes.",
                "Write a one-page summary with the key points.",
                "Try a second example without looking at the notes.",
            ],
        }

    def _ensure_target_language(
        self,
        text: str,
        topic: str,
        language_name: str,
        language_code: str,
    ) -> str:
        if language_code == "en":
            return text

        # For Hindi, ensure Devanagari is present; if not, translate/enforce.
        if language_code == "hi" and not self._has_devanagari(text):
            print("⚠️ Narration is not in Devanagari. Enforcing Hindi translation...")
            translated = self._translate_text(text, language_name, language_code)
            if translated and self._has_devanagari(translated):
                return translated

            # Safe fallback in Hindi if translation still fails
            return (
                f"आज हम {topic} विषय को सरल भाषा में समझेंगे। "
                "पहले इसकी बुनियादी अवधारणा देखेंगे। "
                "फिर चरणबद्ध तरीके से एक उदाहरण समझेंगे। "
                "अंत में इसके व्यावहारिक उपयोगों पर चर्चा करेंगे।"
            )

        # For other non-English languages, translate once to enforce target language.
        translated = self._translate_text(text, language_name, language_code)
        return translated or text

    def _translate_text(self, text: str, language_name: str, language_code: str) -> str:
        prompt = f"""
Translate the following educational narration into {language_name}.

Rules:
- Output only translated narration text.
- Keep 6-12 short conversational sentences.
- No markdown, no bullets, no headings.
- Keep meaning accurate.
- If target language is Hindi, use Devanagari script only.

Text:
{text}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=900,
            )
            translated = response.choices[0].message.content.strip()
            if translated.startswith("```"):
                translated = translated.split("\n", 1)[-1]
            if translated.endswith("```"):
                translated = translated.rsplit("\n", 1)[0]
            return translated
        except Exception as e:
            print(f"❌ Translation to {language_code} failed: {e}")
            return ""

    def _has_devanagari(self, text: str) -> bool:
        # Devanagari Unicode block: U+0900 to U+097F
        return bool(re.search(r"[\u0900-\u097F]", text))

    # ---------------- CLEANING METHODS ---------------- #

    def _clean_markdown(self, code: str) -> str:
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        return code.strip()

    def _ensure_import(self, code: str) -> str:
        lines = code.split("\n")
        import_line = None
        other_lines = []

        for line in lines:
            if "from manim import" in line:
                import_line = line
            else:
                other_lines.append(line)

        if not import_line:
            import_line = "from manim import *"

        return import_line + "\n" + "\n".join(other_lines)

    def _fix_class_name(self, code: str) -> str:
        return re.sub(r'class\s+\w+\(Scene\):', 'class DemoScene(Scene):', code)

    def _final_cleanup(self, code: str) -> str:
        # Remove trailing spaces and weird artifacts
        lines = [line.rstrip() for line in code.split("\n")]

        # Remove empty excessive lines
        cleaned = []
        prev_empty = False
        for line in lines:
            if line == "":
                if not prev_empty:
                    cleaned.append(line)
                prev_empty = True
            else:
                cleaned.append(line)
                prev_empty = False

        return "\n".join(cleaned)

    # ---------------- FALLBACK ---------------- #

    def _fallback_code(self, topic: str) -> str:
        return f"""from manim import *

class DemoScene(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"

        # 1. Title Introduction
        title = Text('{topic}', font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        line = Line(LEFT*2.5, RIGHT*2.5, color=BLUE)
        line.next_to(title, DOWN*0.3)
        self.play(Create(line))
        self.wait(0.5)

        # 2. Concept Breakdown
        concept = Text('Understanding the core idea', font_size=24, color=GREY_B)
        concept.next_to(line, DOWN, buff=0.5)
        self.play(FadeIn(concept))
        self.wait(1)

        box = SurroundingRectangle(concept, color=YELLOW)
        self.play(Create(box))
        self.wait(1)

        # 3. Stacked List using VGroup and arrange()
        step1 = Text('Step 1: Basics', font_size=24, color=RED)
        step2 = Text('Step 2: Process', font_size=24, color=BLUE)
        step3 = Text('Step 3: Result', font_size=24, color=GREEN)

        group = VGroup(step1, step2, step3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        group.next_to(concept, DOWN, buff=1.0)
        
        self.play(FadeIn(group))
        self.wait(2)

        # 4. Clear Screen before next scene
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)
"""

    # ---------------- LEGACY ---------------- #

    def generate_teaching_script(self, topic: str) -> dict:
        """Generate a lightweight teaching script for legacy callers.

        For now this wraps the narration text in a simple structure
        that older parts of the code expect.
        """

        narration = self.generate_narration_text(topic, "English", "en")
        return {
            "title": topic.title(),
            "concept": topic,
            "narration": narration,
        }


_llm_service = None


def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMServiceManager()
    return _llm_service


def generate_teaching_script(topic: str) -> dict:
    return get_llm_service().generate_teaching_script(topic)


def generate_manim_from_script(script: dict) -> str:
    return get_llm_service().generate_manim_video_code(script.get("title", "Topic"))


def generate_narration_text(
    topic: str,
    language_name: str = "English",
    language_code: str = "en",
) -> str:
    """Convenience wrapper for narration generation."""
    return get_llm_service().generate_narration_text(topic, language_name, language_code)