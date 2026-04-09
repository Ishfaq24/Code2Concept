from manim import *

class DemoScene(Scene):
    def construct(self):
        # --- SECTION 1: Introduction ---
        title = Text("What is Machine Learning?", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        subtitle = Text("Teaching computers to learn from data", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(subtitle))

        # --- SECTION 2: Traditional Programming vs ML ---
        label_trad = Text("Traditional Programming", font_size=28)
        label_trad.to_edge(UP)
        self.play(Write(label_trad))

        trad_data = Text("Data", font_size=24)
        trad_data.next_to(label_trad, DOWN, buff=0.7).shift(LEFT * 3)

        trad_rules = Text("Rules", font_size=24)
        trad_rules.next_to(trad_data, RIGHT, buff=1.5)

        trad_ans = Text("Answer", font_size=24)
        trad_ans.next_to(trad_rules, RIGHT, buff=1.5)

        arrow1 = Arrow(trad_data.get_right(), trad_rules.get_left())
        arrow2 = Arrow(trad_rules.get_right(), trad_ans.get_left())

        self.play(FadeIn(trad_data), FadeIn(trad_rules), FadeIn(trad_ans))
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        # --- SECTION 3: How ML Works ---
        label_ml = Text("Machine Learning", font_size=28)
        label_ml.to_edge(UP)
        self.play(Write(label_ml))

        ml_data = Text("Data", font_size=24)
        ml_data.next_to(label_ml, DOWN, buff=0.7).shift(LEFT * 3)

        ml_ans = Text("Answers", font_size=24)
        ml_ans.next_to(ml_data, RIGHT, buff=1.5)

        ml_model = Text("Model (The Rules)", font_size=24)
        ml_model.next_to(ml_data, DOWN, buff=1.5)

        arrow_d_a = Arrow(ml_data.get_right(), ml_ans.get_left())
        arrow_d_m = Arrow(ml_data.get_bottom(), ml_model.get_top())
        arrow_a_m = Arrow(ml_ans.get_bottom(), ml_model.get_top())

        self.play(FadeIn(ml_data), FadeIn(ml_ans))
        self.play(GrowArrow(arrow_d_a))
        self.wait(1)

        self.play(FadeIn(ml_model))
        self.play(GrowArrow(arrow_d_m), GrowArrow(arrow_a_m))

        box = SurroundingRectangle(ml_model, color=YELLOW)
        self.play(Create(box))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        # --- SECTION 4: Final Summary ---
        summary_title = Text("The Core Idea", font_size=40)
        summary_title.to_edge(UP)
        self.play(Write(summary_title))

        line1 = Text("Input Data + Target Answers", font_size=28)
        line2 = Text("→ Algorithm finds the pattern", font_size=28)
        line3 = Text("→ Model predicts new data", font_size=28)

        summary_group = VGroup(line1, line2, line3)
        summary_group.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        summary_group.next_to(summary_title, DOWN, buff=1.0)

        self.play(Write(line1))
        self.wait(1)
        self.play(Write(line2))
        self.wait(1)
        self.play(Write(line3))
        self.wait(3)

        self.play(FadeOut(*self.mobjects))