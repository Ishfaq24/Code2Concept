from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("Understanding Neural Networks", font_size=40)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        concept1 = Text("1. The Basic Unit: The Neuron", font_size=32)
        concept1.to_edge(UP)
        self.play(Write(concept1))
        self.wait(1)

        neuron_circle = Circle(radius=0.7, color=BLUE)
        neuron_circle.shift(LEFT * 3)
        self.play(Create(neuron_circle))
        self.wait(1)

        neuron_label = Text("Neuron", font_size=24)
        neuron_label.move_to(neuron_circle.get_center())
        self.play(Write(neuron_label))
        self.wait(1)

        input_text = Text("Inputs (x)", font_size=24)
        input_text.next_to(neuron_circle, LEFT, buff=1)
        self.play(Write(input_text))
        self.wait(1)

        arrow_in = Arrow(input_text.get_right(), neuron_circle.get_left(), color=WHITE)
        self.play(Create(arrow_in))
        self.wait(1)

        weight_text = Text("Weight (w)", font_size=20, color=YELLOW)
        weight_text.next_to(arrow_in, UP, buff=0.1)
        self.play(Write(weight_text))
        self.wait(1)

        output_text = Text("Output (y)", font_size=24)
        output_text.next_to(neuron_circle, RIGHT, buff=1)
        self.play(Write(output_text))
        self.wait(1)

        arrow_out = Arrow(neuron_circle.get_right(), output_text.get_left(), color=WHITE)
        self.play(Create(arrow_out))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        concept2 = Text("2. The Network Architecture", font_size=32)
        concept2.to_edge(UP)
        self.play(Write(concept2))
        self.wait(1)

        layers = VGroup()

        in_layer = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)])
        in_layer.arrange(DOWN, buff=0.5)
        in_layer.shift(LEFT * 4)

        hid_layer = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(4)])
        hid_layer.arrange(DOWN, buff=0.4)
        hid_layer.shift(LEFT * 1)

        out_layer = VGroup(*[Circle(radius=0.3, color=RED) for _ in range(2)])
        out_layer.arrange(DOWN, buff=0.8)
        out_layer.shift(RIGHT * 3)

        in_label = Text("Input Layer", font_size=24).next_to(in_layer, UP, buff=0.5)
        hid_label = Text("Hidden Layer", font_size=24).next_to(hid_layer, UP, buff=0.5)
        out_label = Text("Output Layer", font_size=24).next_to(out_layer, UP, buff=0.5)

        self.play(Create(in_layer), Write(in_label))
        self.wait(1)
        self.play(Create(hid_layer), Write(hid_label))
        self.wait(1)
        self.play(Create(out_layer), Write(out_label))
        self.wait(1)

        all_connections = VGroup()
        for i in in_layer:
            for j in hid_layer:
                all_connections.add(Line(i.get_right(), j.get_left(), stroke_width=1, color=GRAY))

        for i in hid_layer:
            for j in out_layer:
                all_connections.add(Line(i.get_right(), j.get_left(), stroke_width=1, color=GRAY))

        self.play(Create(all_connections), run_time=3)
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        concept3 = Text("3. How it Learns", font_size=32)
        concept3.to_edge(UP)
        self.play(Write(concept3))
        self.wait(1)

        step1 = Text("1. Forward Pass: Make Prediction", font_size=24)
        step2 = Text("2. Calculate Error (Loss)", font_size=24)
        step3 = Text("3. Backpropagation: Adjust Weights", font_size=24)

        steps_group = VGroup(step1, step2, step3).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        steps_group.shift(UP * 1)

        self.play(Write(step1))
        self.wait(1)
        box1 = SurroundingRectangle(step1, color=YELLOW)
        self.play(Create(box1))
        self.wait(2)
        self.play(FadeOut(box1))

        self.play(Write(step2))
        self.wait(1)
        box2 = SurroundingRectangle(step2, color=YELLOW)
        self.play(Create(box2))
        self.wait(2)
        self.play(FadeOut(box2))

        self.play(Write(step3))
        self.wait(1)
        box3 = SurroundingRectangle(step3, color=YELLOW)
        self.play(Create(box3))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        summary = Text("Neural Networks mimic the brain", font_size=30)
        summary.shift(UP * 1)

        detail1 = Text("They learn patterns from data", font_size=24)
        detail2 = Text("By adjusting weights and biases", font_size=24)
        detail3 = Text("To minimize the error", font_size=24)

        details = VGroup(detail1, detail2, detail3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        details.next_to(summary, DOWN, buff=0.8)

        self.play(Write(summary))
        self.wait(1)
        self.play(FadeIn(details))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))