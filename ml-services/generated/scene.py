from manim import *

class DemoScene(Scene):
    def construct(self):
        title = Text("How the Human Brain Works", font_size=40)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        intro_text = Text("The brain is a complex network", font_size=28)
        intro_text.shift(UP * 2)
        self.play(Write(intro_text))
        self.wait(1)

        sub_text = Text("of billions of neurons", font_size=28)
        sub_text.next_to(intro_text, DOWN, buff=0.5)
        self.play(Write(sub_text))
        self.wait(2)
        self.play(FadeOut(intro_text), FadeOut(sub_text))

        neuron_center = Circle(radius=0.5, color=BLUE).shift(LEFT * 3)
        neuron_label = Text("Neuron Body", font_size=24).next_to(neuron_center, UP)
        self.play(Create(neuron_center), Write(neuron_label))
        self.wait(1)

        dendrite = Line(LEFT * 4, LEFT * 3.5, color=WHITE)
        dendrite_label = Text("Dendrite (Input)", font_size=24).next_to(dendrite, LEFT)
        self.play(Create(dendrite), Write(dendrite_label))
        self.wait(1)

        axon = Line(LEFT * 2.5, RIGHT * 1, color=WHITE)
        axon_label = Text("Axon (Transmission)", font_size=24).next_to(axon, DOWN)
        self.play(Create(axon), Write(axon_label))
        self.wait(1)

        synapse = Dot(point=RIGHT * 1, color=YELLOW)
        synapse_label = Text("Synapse (Gap)", font_size=24).next_to(synapse, RIGHT)
        self.play(Create(synapse), Write(synapse_label))
        self.wait(2)

        signal = Dot(color=YELLOW).move_to(LEFT * 4)
        self.play(Write(Text("Signal Flow", font_size=28).to_edge(UP)))
        self.play(signal.animate.move_to(LEFT * 3), run_time=1)
        self.play(signal.animate.move_to(LEFT * 2), run_time=1)
        self.play(signal.animate.move_to(RIGHT * 1), run_time=1)
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        brain_title = Text("Major Brain Regions", font_size=40)
        brain_title.to_edge(UP)
        self.play(Write(brain_title))
        self.wait(1)

        forebrain = Rectangle(width=3, height=1, color=RED).shift(UP * 1)
        forebrain_txt = Text("Forebrain: Logic & Planning", font_size=24).move_to(forebrain.get_center())
        self.play(Create(forebrain), Write(forebrain_txt))
        self.wait(2)

        midbrain = Rectangle(width=3, height=1, color=GREEN).next_to(forebrain, DOWN, buff=0.8)
        midbrain_txt = Text("Midbrain: Sensory Relay", font_size=24).move_to(midbrain.get_center())
        self.play(Create(midbrain), Write(midbrain_txt))
        self.wait(2)

        hindbrain = Rectangle(width=3, height=1, color=BLUE).next_to(midbrain, DOWN, buff=0.8)
        hindbrain_txt = Text("Hindbrain: Vital Functions", font_size=24).move_to(hindbrain.get_center())
        self.play(Create(hindbrain), Write(hindbrain_txt))
        self.wait(2)

        box = SurroundingRectangle(forebrain, color=YELLOW)
        self.play(Create(box))
        self.wait(1)
        self.play(FadeOut(box))
        self.wait(1)
        self.play(FadeOut(*self.mobjects))

        summary_title = Text("Summary of Working", font_size=40)
        summary_title.to_edge(UP)
        self.play(Write(summary_title))
        self.wait(1)

        step1 = Text("1. Input via Senses", font_size=28)
        step1.shift(UP * 1.5)
        self.play(Write(step1))
        self.wait(1)

        step2 = Text("2. Electrical Signal Travel", font_size=28)
        step2.next_to(step1, DOWN, buff=0.6)
        self.play(Write(step2))
        self.wait(1)

        step3 = Text("3. Chemical Transfer (Synapse)", font_size=28)
        step3.next_to(step2, DOWN, buff=0.6)
        self.play(Write(step3))
        self.wait(1)

        step4 = Text("4. Processing & Response", font_size=28)
        step4.next_to(step3, DOWN, buff=0.6)
        self.play(Write(step4))
        self.wait(2)

        final_box = SurroundingRectangle(VGroup(step1, step2, step3, step4), color=GOLD)
        self.play(Create(final_box))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))