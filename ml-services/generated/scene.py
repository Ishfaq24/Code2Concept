from manim import *

class DemoScene(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a1a"

        # --- SECTION 1: TITLE SLIDE ---
        title = Text("What is an Interpreter?", font_size=40, color="#00FFFF").to_edge(UP)
        underline = Line(LEFT, RIGHT, color=GOLD).scale(3).next_to(title, DOWN, buff=0.2)

        subtitle = Text("Understanding Code Execution", font_size=24, color=LIGHT_GRAY).next_to(underline, DOWN, buff=0.5)

        self.play(Write(title), run_time=1)
        self.play(Create(underline), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.wait(self.wait(2))
        self.play(FadeOut(title), FadeOut(underline), FadeOut(subtitle))

        # --- SECTION 2: THE CONCEPT ---
        concept_title = Text("The Basic Concept", font_size=36, color="#00FFFF").to_edge(UP)
        self.play(Write(concept_title))

        def_text1 = Text("An interpreter is a program", font_size=28, color=WHITE)
        def_text2 = Text("that executes instructions", font_size=28, color=WHITE)
        def_text3 = Text("directly without prior compilation.", font_size=28, color=WHITE)

        def_group = VGroup(def_text1, def_text2, def_text3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        def_group.move_to(ORIGIN).shift(UP*0.5)

        for line in def_group:
            self.play(Write(line), run_time=1)
            self.wait(0.5)

        highlight_box = SurroundingRectangle(def_text3, color=GOLD, buff=0.1)
        self.play(Create(highlight_box))
        self.play(Indicate(def_text3, color=GOLD))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # --- SECTION 3: VISUAL WORKFLOW (THE "ON-THE-FLY" PROCESS) ---
        flow_title = Text("How it Works: Line-by-Line", font_size=36, color="#00FFFF").to_edge(UP)
        self.play(Write(flow_title))

        # Components
        source_code = Rectangle(height=3, width=2, color=WHITE, fill_opacity=0.1)
        source_label = Text("Source Code", font_size=24, color=LIGHT_GRAY).next_to(source_code, UP)

        interpreter_box = RoundedRectangle(corner_radius=0.2, height=2, width=3, color=GOLD, fill_opacity=0.2)
        interpreter_label = Text("Interpreter", font_size=28, color=GOLD).next_to(interpreter_box, UP)

        output_box = Rectangle(height=1, width=2, color=GREEN, fill_opacity=0.1)
        output_label = Text("Output", font_size=24, color=LIGHT_GRAY).next_to(output_box, UP)

        group_layout = VGroup(source_code, interpreter_box, output_box).arrange(RIGHT, buff=2)
        group_layout.center()

        self.play(
            FadeIn(source_code), FadeIn(source_label),
            FadeIn(interpreter_box), FadeIn(interpreter_label),
            FadeIn(output_box), FadeIn(output_label),
            run_time=1.5
        )

        # Code lines
        line1 = Text("print('Hello')", font_size=20, color=WHITE).move_to(source_code.get_center() + UP*0.5)
        line2 = Text("x = 5 + 2", font_size=20, color=WHITE).move_to(source_code.get_center())
        line3 = Text("print(x)", font_size=20, color=WHITE).move_to(source_code.get_center() + DOWN*0.5)

        code_lines = VGroup(line1, line2, line3)
        self.play(Write(code_lines), run_time=1)

        # Animation Loop
        for i in range(3):
            current_line = code_lines[i]

            # Highlight line
            line_box = SurroundingRectangle(current_line, color="#00FFFF", buff=0.05)
            self.play(Create(line_box), run_time=0.5)

            # Move to interpreter
            arrow1 = Arrow(line_box.get_right(), interpreter_box.get_left(), color="#00FFFF")
            self.play(GrowArrow(arrow1), run_time=0.5)

            # Process in interpreter
            self.play(Indicate(interpreter_box, color=GOLD), run_time=0.6)

            # Move to output
            arrow2 = Arrow(interpreter_box.get_right(), output_box.get_left(), color=GREEN)
            self.play(GrowArrow(arrow2), run_time=0.5)

            # Show output
            res_text = Text("Result " + str(i+1), font_size=18, color=GREEN).move_to(output_box.get_center())
            self.play(Write(res_text), run_time=0.5)

            self.play(FadeOut(line_box), FadeOut(arrow1), FadeOut(arrow2), run_time=0.3)
            self.wait(0.5)

        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # --- SECTION 4: COMPARISON (INTERPRETER VS COMPILER) ---
        comp_title = Text("Interpreter vs Compiler", font_size=36, color="#00FFFF").to_edge(UP)
        self.play(Write(comp_title))

        # Table-like layout
        left_col = VGroup(
            Text("Interpreter", font_size=30, color=GOLD),
            Text("• Reads line by line", font_size=24, color=WHITE),
            Text("• Executes immediately", font_size=24, color=WHITE),
            Text("• Slower execution", font_size=24, color=WHITE),
            Text("• Easier debugging", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(LEFT*3)

        right_col = VGroup(
            Text("Compiler", font_size=30, color="#00FFFF"),
            Text("• Translates whole file", font_size=24, color=WHITE),
            Text("• Creates binary file", font_size=24, color=WHITE),
            Text("• Faster execution", font_size=24, color=WHITE),
            Text("• Harder debugging", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT*3)

        self.play(FadeIn(left_col, shift=RIGHT), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(right_col, shift=LEFT), run_time=1)

        # Highlighting a key difference
        diff_box = SurroundingRectangle(left_col[1], color=GOLD)
        self.play(Create(diff_box))
        self.play(Indicate(left_col[1]))
        self.wait(1)
        self.play(FadeOut(diff_box))

        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # --- SECTION 5: CONCLUSION ---
        final_title = Text("Key Takeaway", font_size=40, color=GOLD).to_edge(UP)
        summary = Text(
            "Interpreters provide flexibility\nand speed of development by\nexecuting code on-the-fly.",
            font_size=28,
            color=WHITE,
            t2c={"flexibility": "#00FFFF", "on-the-fly": GOLD},
            line_spacing=1.2
        ).move_to(ORIGIN)

        self.play(Write(final_title))
        self.play(FadeIn(summary, scale=0.8), run_time=1.5)

        # Final Polish
        circle_bg = Circle(radius=3, color=GOLD).set_stroke(opacity=0.2)
        self.play(Create(circle_bg), run_time=2)
        self.wait(3)

        # Outro
        self.play(
            FadeOut(final_title),
            FadeOut(summary),
            FadeOut(circle_bg),
            run_time=1
        )

        closing = Text("Thank You!", font_size=48, color="#00FFFF").move_to(ORIGIN)
        self.play(GrowFromCenter(closing))
        self.wait(2)