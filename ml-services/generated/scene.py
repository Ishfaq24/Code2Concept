from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Merge Sort Algorithm", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        desc1 = Text("Divide and Conquer Strategy", font_size=28)
        desc1.next_to(title, DOWN, buff=0.5)
        self.play(Write(desc1))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        list_vals = [38, 27, 43, 3, 9, 82, 10]
        array_group = VGroup(*[Square(side_length=0.8) for _ in range(len(list_vals))])
        array_group.arrange(RIGHT, buff=0.1)
        array_group.move_to(UP * 2)

        labels = VGroup(*[Text(str(v), font_size=24).move_to(sq.get_center()) for v, sq in zip(list_vals, array_group)])

        self.play(Create(array_group), Write(labels))
        self.wait(1)

        step1_txt = Text("Step 1: Divide into halves", font_size=28)
        step1_txt.next_to(array_group, DOWN, buff=1)
        self.play(Write(step1_txt))
        self.wait(1)

        left_half = VGroup(array_group[0:4], labels[0:4]).copy()
        right_half = VGroup(array_group[4:7], labels[4:7]).copy()

        left_half.shift(LEFT * 2 + DOWN * 1.5)
        right_half.shift(RIGHT * 2 + DOWN * 1.5)

        arrow_l = Arrow(array_group.get_center(), left_half.get_top(), color=BLUE)
        arrow_r = Arrow(array_group.get_center(), right_half.get_top(), color=BLUE)

        self.play(Create(arrow_l), Create(arrow_r))
        self.play(FadeIn(left_half), FadeIn(right_half))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        merge_title = Text("Step 2: Merge and Sort", font_size=40)
        merge_title.to_edge(UP)
        self.play(Write(merge_title))
        self.wait(1)

        unsorted = VGroup(
            Text("[3, 27]", font_size=28),
            Text("[9, 82, 10]", font_size=28)
        ).arrange(RIGHT, buff=2).shift(UP * 1)

        self.play(Write(unsorted))
        self.wait(1)

        sorted_res = Text("[3, 9, 10, 27, 82]", font_size=28, color=GREEN)
        sorted_res.next_to(unsorted, DOWN, buff=1.5)

        merge_arrow = Arrow(unsorted.get_bottom(), sorted_res.get_top(), color=YELLOW)

        self.play(Create(merge_arrow))
        self.play(Write(sorted_res))
        self.wait(2)

        box = SurroundingRectangle(sorted_res, color=YELLOW)
        self.play(Create(box))
        self.wait(1)

        self.play(FadeOut(*self.mobjects))

        summary_title = Text("Merge Sort Summary", font_size=40)
        summary_title.to_edge(UP)
        self.play(Write(summary_title))
        self.wait(1)

        line1 = Text("1. Divide array into halves", font_size=28)
        line1.next_to(summary_title, DOWN, buff=0.8)

        line2 = Text("2. Recursively sort sub-arrays", font_size=28)
        line2.next_to(line1, DOWN, buff=0.4)

        line3 = Text("3. Merge sorted halves together", font_size=28)
        line3.next_to(line2, DOWN, buff=0.4)

        line4 = Text("Time Complexity: O(n log n)", font_size=28, color=YELLOW)
        line4.next_to(line3, DOWN, buff=0.8)

        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.wait(1)
        self.play(Write(line3))
        self.wait(1)
        self.play(Write(line4))
        self.wait(3)