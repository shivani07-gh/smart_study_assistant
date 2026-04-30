from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

def generate_answer(context_chunks, question):

    # 🔥 Better context formatting
    context = "\n\n".join(context_chunks[:5])  # limit + clean

    response = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",

        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI tutor. Answer clearly using the given context."
            },
            {
                "role": "user",
                "content": f"""
Use the context below to answer the question.

IMPORTANT:
- Answer using ONLY the context
- If partially available, still try to answer
- Do NOT say "I don't know" unless absolutely no info

--------------------
CONTEXT:
{context}
--------------------

QUESTION:
{question}

ANSWER:
"""
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content.strip()