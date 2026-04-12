from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Binary Search Algorithm", font_size=40)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        desc1 = Text("Efficiently find a value", font_size=28)
        desc2 = Text("Requires a SORTED array", font_size=28)
        desc_group = VGroup(desc1, desc2).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        desc_group.move_to(ORIGIN)

        self.play(Write(desc1))
        self.wait(1)
        self.play(Write(desc2))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        array_vals = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        squares = VGroup(*[Square(side_length=0.8) for _ in array_vals])
        squares.arrange(RIGHT, buff=0.1)

        labels = VGroup(*[Text(str(v), font_size=24) for v in array_vals])
        for i in range(len(labels)):
            labels[i].move_to(squares[i].get_center())

        array_group = VGroup(squares, labels).center()

        target_text = Text("Target: 70", font_size=28).next_to(array_group, UP, buff=1)

        self.play(Create(squares), Write(labels))
        self.play(Write(target_text))
        self.wait(1)

        low_ptr = Arrow(start=UP, end=DOWN, color=BLUE).next_to(squares[0], DOWN)
        low_label = Text("Low", font_size=20, color=BLUE).next_to(low_ptr, DOWN)

        high_ptr = Arrow(start=UP, end=DOWN, color=RED).next_to(squares[-1], DOWN)
        high_label = Text("High", font_size=20, color=RED).next_to(high_ptr, DOWN)

        self.play(Create(low_ptr), Write(low_label))
        self.play(Create(high_ptr), Write(high_label))
        self.wait(1)

        mid_idx = 4
        mid_box = SurroundingRectangle(squares[mid_idx], color=YELLOW)
        mid_label = Text("Mid", font_size=20, color=YELLOW).next_to(mid_box, UP)

        self.play(Create(mid_box), Write(mid_label))
        self.wait(1)

        compare_text = Text("50 < 70: Search Right", font_size=28).next_to(array_group, DOWN, buff=1.5)
        self.play(Write(compare_text))
        self.wait(2)

        self.play(FadeOut(mid_box), FadeOut(mid_label), FadeOut(compare_text))
        self.play(low_ptr.animate.next_to(squares[5], DOWN), low_label.animate.next_to(low_ptr, DOWN))
        self.wait(1)

        mid_idx_2 = 6
        mid_box_2 = SurroundingRectangle(squares[mid_idx_2], color=YELLOW)
        mid_label_2 = Text("Mid", font_size=20, color=YELLOW).next_to(mid_box_2, UP)

        self.play(Create(mid_box_2), Write(mid_label_2))
        self.wait(1)

        found_text = Text("70 == 70: Found!", font_size=28, color=GREEN).next_to(array_group, DOWN, buff=1.5)
        self.play(Write(found_text))
        self.wait(3)

        self.play(FadeOut(*self.mobjects))

        summary_title = Text("Complexity", font_size=40)
        summary_title.move_to(UP * 2)

        time_comp = Text("Time Complexity: O(log n)", font_size=28).next_to(summary_title, DOWN, buff=1)
        space_comp = Text("Space Complexity: O(1)", font_size=28).next_to(time_comp, DOWN, buff=0.5)

        self.play(Write(summary_title))
        self.wait(1)
        self.play(Write(time_comp))
        self.wait(1)
        self.play(Write(space_comp))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))