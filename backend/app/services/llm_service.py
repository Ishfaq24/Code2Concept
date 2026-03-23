from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_manim_code(topic: str):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Generate simple Manim code for: {topic}"
        )
        return response.text

    except Exception as e:
        print("Gemini failed:", e)

        # 🔥 FALLBACK CODE (VERY IMPORTANT)
        return """
from manim import *

class DemoScene(Scene):
    def construct(self):
        text = Text("Binary Search").scale(1.2)
        self.play(Write(text))
        self.wait(2)
"""