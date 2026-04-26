from manim import *

class DemoScene(Scene):
    def construct(self):
        # --- PART 1: INTRODUCTION ---
        title = Text("Understanding Neural Networks", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        intro_text1 = Text("Inspired by the human brain", font_size=28)
        intro_text1.next_to(title, DOWN, buff=1)
        self.play(Write(intro_text1))
        self.wait(1)

        intro_text2 = Text("Processes data in layers", font_size=28)
        intro_text2.next_to(intro_text1, DOWN, buff=0.5)
        self.play(Write(intro_text2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        # --- PART 2: THE NEURON (PERCEPTRON) ---
        neuron_title = Text("The Basic Unit: The Neuron", font_size=40)
        neuron_title.to_edge(UP)
        self.play(Write(neuron_title))
        self.wait(1)

        # Visuals for Neuron
        input_node = Circle(radius=0.4, color=BLUE).shift(LEFT * 3)
        input_label = Text("Input (x)", font_size=24).next_to(input_node, LEFT)
        self.play(Create(input_node), Write(input_label))
        self.wait(1)

        neuron_node = Circle(radius=0.6, color=WHITE).shift(ORIGIN)
        neuron_label = Text("Neuron", font_size=24).next_to(neuron_node, UP)
        self.play(Create(neuron_node), Write(neuron_label))
        self.wait(1)

        conn_arrow = Arrow(input_node.get_right(), neuron_node.get_left(), buff=0.1)
        weight_label = Text("Weight (w)", font_size=24).next_to(conn_arrow, UP)
        self.play(Create(conn_arrow), Write(weight_label))
        self.wait(1)

        output_node = Circle(radius=0.4, color=GREEN).shift(RIGHT * 3)
        output_label = Text("Output (y)", font_size=24).next_to(output_node, RIGHT)
        self.play(Create(output_node), Write(output_label))
        self.wait(1)

        out_arrow = Arrow(neuron_node.get_right(), output_node.get_left(), buff=0.1)
        self.play(Create(out_arrow))
        self.wait(1)

        # Highlight Process
        process_text = Text("Sum(x * w) + bias -> Activation", font_size=28)
        process_text.next_to(neuron_node, DOWN, buff=1)
        self.play(Write(process_text))

        box = SurroundingRectangle(process_text, color=YELLOW)
        self.play(Create(box))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        # --- PART 3: NETWORK ARCHITECTURE ---
        net_title = Text("Network Architecture", font_size=40)
        net_title.to_edge(UP)
        self.play(Write(net_title))
        self.wait(1)

        # Layers
        layer1_title = Text("Input Layer", font_size=28).shift(LEFT * 4 + UP * 1)
        layer2_title = Text("Hidden Layer", font_size=28).shift(ORIGIN + UP * 1)
        layer3_title = Text("Output Layer", font_size=28).shift(RIGHT * 4 + UP * 1)

        self.play(Write(layer1_title), Write(layer2_title), Write(layer3_title))
        self.wait(1)

        # Nodes
        in_nodes = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)])
        in_nodes.arrange(DOWN, buff=0.5).shift(LEFT * 4)

        hid_nodes = VGroup(*[Circle(radius=0.3, color=WHITE) for _ in range(4)])
        hid_nodes.arrange(DOWN, buff=0.4).shift(ORIGIN)

        out_nodes = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(2)])
        out_nodes.arrange(DOWN, buff=0.8).shift(RIGHT * 4)

        self.play(Create(in_nodes))
        self.wait(1)
        self.play(Create(hid_nodes))
        self.wait(1)
        self.play(Create(out_nodes))
        self.wait(1)

        # Connections
        connections = VGroup()
        for i in in_nodes:
            for j in hid_nodes:
                connections.add(Line(i.get_right(), j.get_left(), stroke_width=1, color=GRAY))

        for j in hid_nodes:
            for k in out_nodes:
                connections.add(Line(j.get_right(), k.get_left(), stroke_width=1, color=GRAY))

        self.play(Create(connections), run_time=3)
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        # --- PART 4: SUMMARY ---
        sum_title = Text("How it Learns", font_size=40)
        sum_title.to_edge(UP)
        self.play(Write(sum_title))
        self.wait(1)

        step1 = Text("1. Forward Pass: Predicts result", font_size=28)
        step2 = Text("2. Loss Function: Measures error", font_size=28)
        step3 = Text("3. Backpropagation: Adjusts weights", font_size=28)

        summary_group = VGroup(step1, step2, step3).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        summary_group.shift(DOWN * 0.5)

        self.play(Write(step1))
        self.wait(1)
        self.play(Write(step2))
        self.wait(1)
        self.play(Write(step3))
        self.wait(2)

        final_box = SurroundingRectangle(summary_group, color=GOLD)
        self.play(Create(final_box))
        self.wait(3)