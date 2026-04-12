import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#temporaray
print("API KEY:", os.getenv("GROQ_API_KEY"))
#temporary
def generate_answer(context, question):
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",   # fast + best
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content