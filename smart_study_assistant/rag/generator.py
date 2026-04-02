import os
from dotenv import load_dotenv
import google.generativeai as genai

# 🔥 Load .env file
load_dotenv()

# 🔑 Get API key correctly
api_key = os.getenv("GEMINI_API_KEY")

# 🧪 Debug
print("API KEY:", api_key)

# 🚨 Safety check
if not api_key:
    raise ValueError("API KEY not found. Check your .env file")

# 🔌 Configure Gemini
genai.configure(api_key=api_key)

# 🤖 Model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")


def generate_answer(query, context_chunks):
    context = "\n".join(context_chunks)

    prompt = f"""
    You are a helpful study assistant.

    Answer strictly ONLY from the given context.
    If the answer is not present, reply exactly:
    "Not in provided document"

    Do not guess. Do not add extra info.

    Context:
    {context}

    Question:
    {query}
    """

    response = model.generate_content(prompt)
    return response.text.strip()