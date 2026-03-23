# ================================
# TEACHING SCRIPT GENERATOR
# ================================

def generate_teaching_script(topic: str):
    topic_lower = topic.lower()

    if "binary search" in topic_lower:
        return {
            "title": "Binary Search",
            "steps": [
                "Binary search works on sorted arrays",
                "Find the middle element",
                "Compare target with middle",
                "Eliminate half of the array",
                "Repeat until found"
            ]
        }

    elif "ai" in topic_lower:
        return {
            "title": "Artificial Intelligence",
            "steps": [
                "AI means machines that can think",
                "It mimics human intelligence",
                "Used in real-world applications",
                "Uses data and algorithms",
                "Improves over time"
            ]
        }

    else:
        return {
            "title": topic.title(),
            "steps": [
                f"{topic.title()} is an important concept",
                "It is widely used",
                "It helps solve problems",
                "It has real-world applications"
            ]
        }


# ================================
# MANIM CODE GENERATOR
# ================================

def generate_manim_from_script(script: dict) -> str:
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