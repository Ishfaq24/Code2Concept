from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

response = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[
        {
            "role": "user",
            "content": "Hello! Explain what an LLM is in simple words."
        }
    ],
    temperature=0.5,
    max_tokens=200
)

print(response.choices[0].message.content)