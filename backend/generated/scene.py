
from manim import *

class DemoScene(Scene):
    def construct(self):
        text = Text("Binary Search").scale(1.2)
        self.play(Write(text))
        self.wait(2)
