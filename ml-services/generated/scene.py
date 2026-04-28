from manim import *

class DemoScene(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a1a"

        # --- SECTION 1: TITLE SLIDE ---
        title = Text("Neural Networks", font_size=40, color="#00FFFF").shift(UP * 0.5)
        subtitle = Text("Mimicking the Human Brain", font_size=24, color=LIGHT_GRAY).next_to(title, DOWN, buff=0.4)

        underline = Line(start=LEFT*2, end=RIGHT*2, color=GOLD).next_to(subtitle, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.play(Create(underline), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(underline))

        # --- SECTION 2: THE BIOLOGICAL ANALOGY ---
        concept_title = Text("The Inspiration", font_size=32, color="#00FFFF").to_edge(UP)
        self.play(Write(concept_title))

        neuron_circle = Circle(radius=1, color=GOLD, fill_opacity=0.2).shift(LEFT * 3)
        neuron_label = Text("Biological\nNeuron", font_size=20, color=WHITE).next_to(neuron_circle, DOWN)

        axon_line = Line(neuron_circle.get_right(), RIGHT * 1, color=WHITE)
        synapse_dot = Dot(point=RIGHT * 1, color=GOLD)

        bio_group = VGroup(neuron_circle, neuron_label, axon_line, synapse_dot).center()

        self.play(DrawBorderThenFill(neuron_circle), Write(neuron_label), run_time=1)
        self.play(Create(axon_line), FadeIn(synapse_dot), run_time=1)
        self.wait(1)

        self.play(FadeOut(bio_group), FadeOut(concept_title))

        # --- SECTION 3: THE ARTIFICIAL NEURON (PERCEPTRON) ---
        concept_title_2 = Text("The Artificial Neuron", font_size=32, color="#00FFFF").to_edge(UP)
        self.play(Write(concept_title_2))

        # Inputs
        inputs = VGroup(*[Circle(radius=0.3, color=BLUE, fill_opacity=0.5) for _ in range(3)])
        inputs.arrange(DOWN, buff=0.5).shift(LEFT * 4)
        input_labels = VGroup(*[Text(f"x{i+1}", font_size=20) for i in range(3)])
        for i in range(3):
            input_labels[i].next_to(inputs[i], LEFT, buff=0.3)

        # Weights/Connections
        neuron_body = Circle(radius=0.7, color=GOLD, fill_opacity=0.3).shift(RIGHT * 0)
        neuron_label_2 = Text("Sum & Activate", font_size=18, color=WHITE).move_to(neuron_body.get_center())

        connections = VGroup(*[Line(inputs[i].get_right(), neuron_body.get_left(), color=GRAY_A) for i in range(3)])

        # Output
        output_node = Circle(radius=0.3, color=GREEN, fill_opacity=0.5).shift(RIGHT * 4)
        output_label = Text("Output (y)", font_size=20).next_to(output_node, RIGHT)
        output_line = Line(neuron_body.get_right(), output_node.get_left(), color=WHITE)

        self.play(FadeIn(inputs, shift=RIGHT), Write(input_labels), run_time=1)
        self.play(Create(connections), run_time=1)
        self.play(DrawBorderThenFill(neuron_body), Write(neuron_label_2), run_time=1)
        self.play(Create(output_line), FadeIn(output_node), Write(output_label), run_time=1)

        # Highlight the process
        box = SurroundingRectangle(neuron_body, color=YELLOW, buff=0.2)
        self.play(Create(box), run_time=0.8)
        self.play(Indicate(box), run_time=1)
        self.wait(2)

        self.play(FadeOut(inputs), FadeOut(input_labels), FadeOut(connections),
                  FadeOut(neuron_body), FadeOut(neuron_label_2), FadeOut(output_node),
                  FadeOut(output_label), FadeOut(output_line), FadeOut(box), FadeOut(concept_title_2))

        # --- SECTION 4: THE FULL NETWORK ---
        concept_title_3 = Text("The Neural Network Architecture", font_size=32, color="#00FFFF").to_edge(UP)
        self.play(Write(concept_title_3))

        def create_layer(n, pos, color):
            layer = VGroup(*[Circle(radius=0.25, color=color, fill_opacity=0.6) for _ in range(n)])
            layer.arrange(DOWN, buff=0.4).move_to(pos)
            return layer

        layer1 = create_layer(3, LEFT * 3, BLUE)
        layer2 = create_layer(4, 0, GOLD)
        layer3 = create_layer(2, RIGHT * 3, GREEN)

        # Connections between layers
        all_conns = VGroup()
        for n1 in layer1:
            for n2 in layer2:
                all_conns.add(Line(n1.get_right(), n2.get_left(), stroke_width=1, color=GRAY_B))
        for n2 in layer2:
            for n3 in layer3:
                all_conns.add(Line(n2.get_right(), n3.get_left(), stroke_width=1, color=GRAY_B))

        self.play(FadeIn(layer1, shift=RIGHT), run_time=0.8)
        self.play(Create(all_conns), run_time=2)
        self.play(FadeIn(layer2, shift=RIGHT), run_time=0.8)
        self.play(FadeIn(layer3, shift=RIGHT), run_time=0.8)

        # Flow Animation
        flow_dots = VGroup()
        for line in all_conns:
            dot = Dot(line.get_start(), radius=0.05, color=WHITE)
            flow_dots.add(dot)

        self.play(
            *[MoveAlongPath(dot, line) for dot, line in zip(flow_dots, all_conns)],
            run_time=2, rate_func=linear
        )
        self.play(FadeOut(flow_dots))
        self.wait(2)

        self.play(FadeOut(layer1), FadeOut(layer2), FadeOut(layer3), FadeOut(all_conns), FadeOut(concept_title_3))

        # --- SECTION 5: KEY TAKEAWAY ---
        final_title = Text("How it Learns", font_size=32, color="#00FFFF").to_edge(UP)
        self.play(Write(final_title))

        points = VGroup(
            Text("1. Forward Pass: Predicts output", font_size=24, color=WHITE),
            Text("2. Loss Function: Measures error", font_size=24, color=WHITE),
            Text("3. Backpropagation: Adjusts weights", font_size=24, color=WHITE),
            Text("4. Iteration: Improves accuracy", font_size=24, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(LEFT * 1)

        for point in points:
            self.play(Write(point), run_time=1)
            self.play(Indicate(point, color=GOLD), run_time=0.5)
            self.wait(0.5)

        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # --- FINAL CLOSING ---
        closing_text = Text("The Foundation of Modern AI", font_size=30, color=GOLD)
        self.play(GrowFromCenter(closing_text), run_time=1.5)
        self.play(Indicate(closing_text), run_time=1)
        self.wait(2)
        self.play(ShrinkToCenter(closing_text), run_time=1)