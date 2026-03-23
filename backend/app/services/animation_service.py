def generate_animation_code(research_data: str):
    prompt = f"""
    Convert this into Manim Python animation code:

    {research_data}

    Rules:
    - Class: DemoScene
    - Show title
    - Show steps visually
    - Use shapes/arrays
    - Keep it clean
    """

    # You can use same Gemini or later upgrade model
    from google import genai
    client = genai.Client()

    res = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return res.text