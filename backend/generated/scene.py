
from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Binary Search").scale(1.2).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        
        step0 = Text("Binary search works on sorted arrays").scale(0.5)
        step0.next_to(title, DOWN*1)
        self.play(Write(step0))
        self.wait(1)
        
        step1 = Text("Find the middle element").scale(0.5)
        step1.next_to(title, DOWN*2)
        self.play(Write(step1))
        self.wait(1)
        
        step2 = Text("Compare target with middle").scale(0.5)
        step2.next_to(title, DOWN*3)
        self.play(Write(step2))
        self.wait(1)
        
        step3 = Text("Eliminate half of the array").scale(0.5)
        step3.next_to(title, DOWN*4)
        self.play(Write(step3))
        self.wait(1)
        
        step4 = Text("Repeat until found").scale(0.5)
        step4.next_to(title, DOWN*5)
        self.play(Write(step4))
        self.wait(1)
        

        self.wait(2)
