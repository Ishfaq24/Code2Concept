from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_research(topic: str):
    prompt = f"""
    Explain the topic "{topic}" in structured JSON format.

    Include:
    - title
    - concept
    - steps (list)
    - simple example

    Return ONLY JSON.
    """

    try:
        res = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return res.text
    except:
        return None