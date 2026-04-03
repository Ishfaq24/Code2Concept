from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Introduction to Machine Learning", color=CYAN, font_size=48)
        definition = Text(
            "A subset of AI that enables computers to learn patterns\nfrom data and make predictions without explicit programming.",
            font_size=28,
            line_spacing=1.5,
            color=WHITE
        ).next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(definition, shift=UP))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(definition))

        steps_data = [
            ("Step 1: Data Collection", "Gather diverse, high-quality datasets\n(Historical records, sensor readings)", CYAN, Write),
            ("Step 2: Data Preprocessing", "Clean data, handle missing values,\nand normalize scales to remove noise", YELLOW, FadeIn),
            ("Step 3: Choosing the Model", "Select algorithm: Supervised (labeled)\nor Unsupervised (clustering)", GREEN, GrowFromCenter),
            ("Step 4: Training the Model", "Adjust internal weights to minimize\nerror between prediction and outcome", RED, Write),
            ("Step 5: Evaluation & Testing", "Use a separate test set to measure\naccuracy and generalizability", BLUE, FadeIn),
            ("Step 6: Hyperparameter Tuning", "Fine-tune settings like learning rate\nto prevent over/underfitting", PURPLE, GrowFromCenter),
            ("Step 7: Deployment & Monitoring", "Integrate into real-world apps and\nupdate with new incoming data", ORANGE, Write),
        ]

        for i, (s_title, s_desc, s_color, s_anim) in enumerate(steps_data):
            step_title = Text(s_title, color=s_color, font_size=36).shift(UP * 1)
            step_desc = Text(s_desc, font_size=24, color=WHITE).next_to(step_title, DOWN, buff=0.5)
            
            group = VGroup(step_title, step_desc)
            
            if s_anim == Write:
                self.play(Write(step_title))
                self.play(Write(step_desc))
            elif s_anim == FadeIn:
                self.play(FadeIn(group, shift=RIGHT))
            elif s_anim == GrowFromCenter:
                self.play(GrowFromCenter(step_title))
                self.play(FadeIn(step_desc))

            self.wait(3)
            self.play(FadeOut(group, shift=LEFT))

        final_text = Text("Machine Learning Pipeline Complete", color=CYAN, font_size=42)
        self.play(Write(final_text))
        self.play(Indicate(final_text))
        self.wait(2)
        self.play(FadeOut(final_text))