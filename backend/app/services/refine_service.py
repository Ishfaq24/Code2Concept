def refine_code(code: str):
    prompt = f"""
    Fix and improve this Manim code:

    {code}

    Ensure:
    - No syntax errors
    - Proper animations
    - Runs correctly
    - Clean structure

    Return ONLY code.
    """

    from google import genai
    client = genai.Client()

    res = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return res.text