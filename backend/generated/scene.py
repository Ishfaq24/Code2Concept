
from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Machine Learning").scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        
        step0 = Text("Machine Learning helps solve real-world problems").scale(0.5)
        step0.next_to(title, DOWN*1)
        self.play(Write(step0))
        self.wait(1)
        
        step1 = Text("Understanding the basics is essential").scale(0.5)
        step1.next_to(title, DOWN*2)
        self.play(Write(step1))
        self.wait(1)
        
        step2 = Text("It has practical applications").scale(0.5)
        step2.next_to(title, DOWN*3)
        self.play(Write(step2))
        self.wait(1)
        
        step3 = Text("Learning step by step builds expertise").scale(0.5)
        step3.next_to(title, DOWN*4)
        self.play(Write(step3))
        self.wait(1)
        
        step4 = Text("Practice and experimentation are key").scale(0.5)
        step4.next_to(title, DOWN*5)
        self.play(Write(step4))
        self.wait(1)
        
        
        self.wait(2)
