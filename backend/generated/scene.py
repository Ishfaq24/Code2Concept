from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Linear Search Algorithm", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        desc = Text("Search for a target value\nin an unsorted list", font_size=28)
        desc.next_to(title, DOWN, buff=0.5)
        self.play(Write(desc))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(desc))

        list_vals = [10, 45, 2, 8, 33]
        target_val = 8

        boxes = VGroup()
        labels = VGroup()

        for val in list_vals:
            rect = Rectangle(width=1, height=1)
            lbl = Text(str(val), font_size=28)
            lbl.move_to(rect.get_center())
            boxes.add(rect)
            labels.add(lbl)

        boxes.arrange(RIGHT, buff=0.2)
        labels.arrange(RIGHT, buff=0.2)

        list_group = VGroup(boxes, labels).center()

        target_text = Text(f"Target: {target_val}", font_size=28, color=YELLOW)
        target_text.next_to(list_group, UP, buff=1)

        self.play(Create(boxes), Write(labels))
        self.play(Write(target_text))
        self.wait(1)

        pointer = Arrow(start=UP, end=DOWN, color=RED).scale(0.7)
        pointer.next_to(boxes[0], UP, buff=0.1)

        self.play(Create(pointer))
        self.wait(0.5)

        for i in range(len(list_vals)):
            box_highlight = SurroundingRectangle(labels[i], color=YELLOW)
            self.play(
                pointer.animate.next_to(boxes[i], UP, buff=0.1),
                Create(box_highlight)
            )

            if list_vals[i] == target_val:
                found_text = Text("Found it!", font_size=28, color=GREEN)
                found_text.next_to(list_group, DOWN, buff=1)
                self.play(Write(found_text))
                self.play(box_highlight.animate.set_color(GREEN))
                self.wait(2)
                self.play(FadeOut(found_text))
                break
            else:
                self.wait(0.5)
                self.play(FadeOut(box_highlight))

        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        summary_title = Text("Complexity", font_size=40)
        summary_title.to_edge(UP)
        self.play(Write(summary_title))
        self.wait(1)

        time_comp = Text("Time Complexity: O(n)", font_size=28)
        time_comp.next_to(summary_title, DOWN, buff=0.8)
        self.play(Write(time_comp))
        self.wait(1)

        space_comp = Text("Space Complexity: O(1)", font_size=28)
        space_comp.next_to(time_comp, DOWN, buff=0.5)
        self.play(Write(space_comp))
        self.wait(2)

        final_note = Text("Checks every element sequentially", font_size=28, color=GRAY)
        final_note.next_to(space_comp, DOWN, buff=1)
        self.play(FadeIn(final_note))
        self.wait(3)