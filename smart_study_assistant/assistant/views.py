from django.shortcuts import render
from django.http import HttpResponse
import os

from .forms import DocumentForm
from .models import Document, ChatHistory

from rag.pdf_loader import extract_text_from_pdf
from rag.chunking import chunk_text
from rag.embeddings import create_embeddings, store_in_faiss

from rag.retrieval import (
    search_similar_chunks,
    save_index,
    load_index,
    save_chunks,
    load_chunks
)

from rag.generator import generate_answer


# 🏠 Home
def home(request):
    return HttpResponse("Smart Study Assistant Running 🚀")


# 📤 Upload PDF
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save()
            file_path = doc.file.path

            # 🔥 STEP 1: Extract text (OCR)
            text = extract_text_from_pdf(file_path)

            print("TEXT LENGTH:", len(text))
            print("TEXT SAMPLE:", text[:200])

            # ❌ agar text hi nahi mila
            if not text or text.strip() == "":
                return HttpResponse("OCR failed ❌ No text extracted")

            # 🔥 STEP 2: Chunk
            chunks = chunk_text(text)

            # 🔥 STEP 3: Clean chunks (VERY IMPORTANT)
            chunks = [c for c in chunks if isinstance(c, str) and c.strip() != ""]

            print("CHUNKS COUNT:", len(chunks))

            # ❌ agar chunks empty
            if not chunks:
                return HttpResponse("No valid chunks found ❌")

            # 🔥 STEP 4: Embeddings
            embeddings = create_embeddings(chunks)

            # 🔥 STEP 5: Store in FAISS
            index = store_in_faiss(embeddings)

            # 📁 Save paths
            index_path = f"media/faiss_{doc.id}.index"
            chunks_path = f"media/chunks_{doc.id}.pkl"

            save_index(index, index_path)
            save_chunks(chunks, chunks_path)

            return render(request, 'assistant/success.html')

    else:
        form = DocumentForm()

    return render(request, 'assistant/upload.html', {'form': form})


# ❓ Ask Question
def ask_question(request):
    documents = Document.objects.all()

    if request.method == 'POST':
        query = request.POST.get('query')
        doc_id = request.POST.get('doc_id')

        if not doc_id:
            return HttpResponse("Please select a document!")

        index_path = f"media/faiss_{doc_id}.index"
        chunks_path = f"media/chunks_{doc_id}.pkl"

        try:
            index = load_index(index_path)
            chunks = load_chunks(chunks_path)
        except:
            return HttpResponse("Index not found. Upload document again.")

        # ❌ agar chunks empty
        if not chunks:
            return HttpResponse("No data found for this document ❌")

        # 🔥 Retrieval
        results = search_similar_chunks(query, index, chunks)

        # ❌ agar results empty
        if not results:
            return HttpResponse("No relevant content found ❌")

        # 🔥 Generate answer
        answer = generate_answer(query, results)

        ChatHistory.objects.create(
            question=query,
            answer=answer
        )

        return render(request, 'assistant/answer.html', {
            'query': query,
            'answer': answer,
            'documents': documents
        })

    return render(request, 'assistant/ask.html', {
        'documents': documents
    })