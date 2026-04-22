from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("What is Binary Search?", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        desc1 = Text("An efficient way to find an item", font_size=28)
        desc1.next_to(title, DOWN, buff=0.5)
        self.play(Write(desc1))
        self.wait(1)

        desc2 = Text("in a SORTED list.", font_size=28, color=YELLOW)
        desc2.next_to(desc1, DOWN, buff=0.4)
        self.play(Write(desc2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        header = Text("How it Works", font_size=35)
        header.to_edge(UP)
        self.play(Write(header))
        self.wait(1)

        nums = [10, 20, 30, 40, 50, 60, 70]
        squares = VGroup(*[Square(side_length=0.8) for _ in range(len(nums))])
        squares.arrange(RIGHT, buff=0.1).shift(UP * 0.5)

        labels = VGroup(*[Text(str(n), font_size=24) for n in nums])
        for i in range(len(labels)):
            labels[i].move_to(squares[i].get_center())

        array_group = VGroup(squares, labels)
        self.play(Create(squares), Write(labels))
        self.wait(1)

        target_text = Text("Target: 60", font_size=28, color=YELLOW)
        target_text.next_to(array_group, DOWN, buff=0.7)
        self.play(Write(target_text))
        self.wait(1)

        low_ptr = Arrow(start=DOWN, end=UP, color=BLUE).scale(0.5)
        low_ptr.next_to(squares[0], DOWN, buff=0.2)
        low_label = Text("Low", font_size=20, color=BLUE).next_to(low_ptr, DOWN, buff=0.1)
        self.play(Create(low_ptr), Write(low_label))
        self.wait(1)

        high_ptr = Arrow(start=DOWN, end=UP, color=RED).scale(0.5)
        high_ptr.next_to(squares[-1], DOWN, buff=0.2)
        high_label = Text("High", font_size=20, color=RED).next_to(high_ptr, DOWN, buff=0.1)
        self.play(Create(high_ptr), Write(high_label))
        self.wait(1)

        mid_idx = 3
        mid_ptr = Arrow(start=DOWN, end=UP, color=GREEN).scale(0.5)
        mid_ptr.next_to(squares[mid_idx], DOWN, buff=0.2)
        mid_label = Text("Mid", font_size=20, color=GREEN).next_to(mid_ptr, DOWN, buff=0.1)

        self.play(Create(mid_ptr), Write(mid_label))
        self.wait(1)

        mid_box = SurroundingRectangle(squares[mid_idx], color=GREEN)
        self.play(Create(mid_box))
        self.wait(1)

        step1 = Text("40 < 60: Discard Left Half", font_size=24)
        step1.next_to(target_text, DOWN, buff=0.5)
        self.play(Write(step1))
        self.wait(2)

        self.play(FadeOut(mid_ptr), FadeOut(mid_label), FadeOut(mid_box), FadeOut(step1))

        low_ptr.next_to(squares[4], DOWN, buff=0.2)
        low_label.next_to(low_ptr, DOWN, buff=0.1)
        self.play(low_ptr.animate.move_to(low_ptr), low_label.animate.move_to(low_label))
        self.wait(1)

        mid_idx_2 = 5
        mid_ptr_2 = Arrow(start=DOWN, end=UP, color=GREEN).scale(0.5)
        mid_ptr_2.next_to(squares[mid_idx_2], DOWN, buff=0.2)
        mid_label_2 = Text("Mid", font_size=20, color=GREEN).next_to(mid_ptr_2, DOWN, buff=0.1)

        self.play(Create(mid_ptr_2), Write(mid_label_2))
        self.wait(1)

        mid_box_2 = SurroundingRectangle(squares[mid_idx_2], color=GREEN)
        self.play(Create(mid_box_2))
        self.wait(1)

        step2 = Text("60 == 60: FOUND!", font_size=24, color=YELLOW)
        step2.next_to(target_text, DOWN, buff=0.5)
        self.play(Write(step2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        summary_title = Text("Summary", font_size=35)
        summary_title.to_edge(UP)
        self.play(Write(summary_title))
        self.wait(1)

        point1 = Text("1. List must be sorted", font_size=28)
        point1.next_to(summary_title, DOWN, buff=0.6)
        self.play(Write(point1))
        self.wait(1)

        point2 = Text("2. Divide search area by half", font_size=28)
        point2.next_to(point1, DOWN, buff=0.4)
        self.play(Write(point2))
        self.wait(1)

        point3 = Text("3. Much faster than linear search", font_size=28)
        point3.next_to(point2, DOWN, buff=0.4)
        self.play(Write(point3))
        self.wait(2)