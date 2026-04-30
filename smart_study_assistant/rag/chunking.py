import re

#  CLEAN TEXT FUNCTION
def clean_text(text):
    if not text:
        return ""

    # removE spaces, newlines 
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


#CHUNK TEXT FUNCTION
def chunk_text(text, chunk_size=500, overlap=100):

    # clean karo
    text = clean_text(text)

    # safety check
    if not isinstance(text, str):
        raise ValueError("Text must be string 😤")

    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size]

        # empty chunk skip karo
        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks