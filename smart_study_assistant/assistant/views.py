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

            text = extract_text_from_pdf(file_path)
            chunks = chunk_text(text)

            if not chunks:
                return HttpResponse("No text found in PDF!")

            embeddings = create_embeddings(chunks)
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

        results = search_similar_chunks(query, index, chunks)
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