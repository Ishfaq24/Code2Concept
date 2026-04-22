from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Hello World Explained", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        code_text = Text("print(\"Hello World!\")", font_size=28)
        code_text.shift(UP * 1)
        self.play(Write(code_text))
        self.wait(1)

        box1 = SurroundingRectangle(code_text, color=YELLOW)
        self.play(Create(box1))
        self.wait(1)

        label1 = Text("The Code", font_size=24)
        label1.next_to(box1, UP, buff=0.3)
        self.play(Write(label1))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        func_text = Text("print", font_size=28)
        func_text.shift(UP * 2)
        self.play(Write(func_text))
        self.wait(1)

        box_func = SurroundingRectangle(func_text, color=BLUE)
        self.play(Create(box_func))
        self.wait(1)

        desc_func = Text("This is a function", font_size=24)
        desc_func.next_to(box_func, DOWN, buff=0.5)
        self.play(Write(desc_func))
        self.wait(1)

        desc_func2 = Text("It tells Python to show text", font_size=24)
        desc_func2.next_to(desc_func, DOWN, buff=0.3)
        self.play(Write(desc_func2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        arg_text = Text("\"Hello World!\"", font_size=28)
        arg_text.shift(UP * 2)
        self.play(Write(arg_text))
        self.wait(1)

        box_arg = SurroundingRectangle(arg_text, color=GREEN)
        self.play(Create(box_arg))
        self.wait(1)

        desc_arg = Text("This is a String", font_size=24)
        desc_arg.next_to(box_arg, DOWN, buff=0.5)
        self.play(Write(desc_arg))
        self.wait(1)

        desc_arg2 = Text("Quotes define the text content", font_size=24)
        desc_arg2.next_to(desc_arg, DOWN, buff=0.3)
        self.play(Write(desc_arg2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        final_code = Text("print(\"Hello World!\")", font_size=28)
        final_code.shift(UP * 1)
        self.play(Write(final_code))
        self.wait(1)

        arrow = Arrow(start=final_code.get_bottom(), end=ORIGIN, buff=0.2)
        self.play(Create(arrow))
        self.wait(1)

        result = Text("Hello World!", font_size=32, color=YELLOW)
        result.shift(DOWN * 1)
        self.play(Write(result))
        self.wait(2)

        summary = Text("You just wrote your first program!", font_size=24)
        summary.next_to(result, DOWN, buff=0.8)
        self.play(FadeIn(summary))
        self.wait(3)