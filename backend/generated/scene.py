from manim import *

class DemoScene(Scene):
    def construct(self):
        # --- SECTION 1: Introduction ---
        title = Text("Decoding the Caesar Cipher", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        intro_text1 = Text("A substitution cipher where letters", font_size=28)
        intro_text1.next_to(title, DOWN, buff=1)

        intro_text2 = Text("are shifted by a fixed number.", font_size=28)
        intro_text2.next_to(intro_text1, DOWN, buff=0.5)

        self.play(Write(intro_text1))
        self.wait(1)
        self.play(Write(intro_text2))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(intro_text1), FadeOut(intro_text2))

        # --- SECTION 2: The Logic ---
        logic_title = Text("The Decoding Rule", font_size=36)
        logic_title.to_edge(UP)
        self.play(Write(logic_title))

        rule_text = Text("Decoded = (Encoded - Shift) mod 26", font_size=32, color=YELLOW)
        rule_text.next_to(logic_title, DOWN, buff=1)
        self.play(Write(rule_text))
        self.wait(2)

        expl1 = Text("1. Find the shift value", font_size=28)
        expl1.next_to(rule_text, DOWN, buff=1)

        expl2 = Text("2. Shift backwards in the alphabet", font_size=28)
        expl2.next_to(expl1, DOWN, buff=0.5)

        expl3 = Text("3. Repeat for every letter", font_size=28)
        expl3.next_to(expl2, DOWN, buff=0.5)

        expl_group = VGroup(expl1, expl2, expl3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        expl_group.next_to(rule_text, DOWN, buff=1)

        self.play(Write(expl1))
        self.wait(1)
        self.play(Write(expl2))
        self.wait(1)
        self.play(Write(expl3))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

        # --- SECTION 3: Visual Example ---
        ex_title = Text("Example: Shift = 3", font_size=36)
        ex_title.to_edge(UP)
        self.play(Write(ex_title))

        # Ciphertext
        cipher_text = Text("Encoded: 'KHOOR'", font_size=32)
        cipher_text.next_to(ex_title, DOWN, buff=1)
        self.play(Write(cipher_text))
        self.wait(1)

        # Alphabet row
        alphabet_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alpha_group = VGroup()
        for char in alphabet_str:
            alpha_group.add(Text(char, font_size=20))
        alpha_group.arrange(RIGHT, buff=0.2)
        alpha_group.next_to(cipher_text, DOWN, buff=1.5)

        # Scale alphabet to fit screen
        alpha_group.scale(0.8)
        self.play(Create(alpha_group))
        self.wait(1)

        # Process first letter 'K'
        target_k = alpha_group[10] # K is index 10
        box_k = SurroundingRectangle(target_k, color=RED)
        self.play(Create(box_k))
        self.wait(1)

        # Arrow moving back 3
        target_h = alpha_group[7] # H is index 7
        arrow = Arrow(start=target_k.get_center(), end=target_h.get_center(), color=YELLOW)
        self.play(Create(arrow))

        box_h = SurroundingRectangle(target_h, color=GREEN)
        self.play(Create(box_h))

        res_text = Text("K -> H", font_size=32)
        res_text.next_to(alpha_group, DOWN, buff=1)
        self.play(Write(res_text))
        self.wait(2)

        # Clear for summary
        self.play(FadeOut(*self.mobjects))

        # --- SECTION 4: Final Summary ---
        summary_title = Text("Summary", font_size=40)
        summary_title.to_edge(UP)
        self.play(Write(summary_title))

        s1 = Text("Identify the Shift Key", font_size=28)
        s2 = Text("Move letters back by that amount", font_size=28)
        s3 = Text("Wrap around from A back to Z", font_size=28)

        summary_group = VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        summary_group.move_to(ORIGIN)

        self.play(FadeIn(s1))
        self.wait(1)
        self.play(FadeIn(s2))
        self.wait(1)
        self.play(FadeIn(s3))
        self.wait(3)

        self.play(FadeOut(*self.mobjects))

        final_msg = Text("Decoded!", font_size=48, color=GREEN)
        self.play(Write(final_msg))
        self.wait(2)