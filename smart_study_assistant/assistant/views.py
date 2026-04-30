from django.shortcuts import render, redirect
from django.http import HttpResponse
import os

from .forms import DocumentForm
from .models import Document, ChatHistory
from django.http import JsonResponse

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


# 🔐 Login
def login_view(request):
    if request.method == "POST":
        return redirect('/dashboard/')
    return render(request, 'assistant/login.html')


# 📊 Dashboard
def dashboard(request):
    docs = Document.objects.all()
    total_docs = docs.count()
    total_questions = ChatHistory.objects.count()

    return render(request, 'assistant/dashboard.html', {
        'documents': docs,
        'total_docs': total_docs,
        'total_questions': total_questions,
    })


# 📤 Upload PDF
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save()
            file_path = doc.file.path

            text = extract_text_from_pdf(file_path)

            if not text.strip():
                return JsonResponse({"error": "No text found"})

            chunks = chunk_text(text)
            chunks = [c for c in chunks if c.strip()]

            embeddings = create_embeddings(chunks)
            index = store_in_faiss(embeddings)

            index_path = f"media/faiss_{doc.id}.index"
            chunks_path = f"media/chunks_{doc.id}.pkl"

            save_index(index, index_path)
            save_chunks(chunks, chunks_path)

            return JsonResponse({
                "message": "Upload success",
                "file_name": doc.file.name,
                "file_size": doc.file.size,
                "id": doc.id
            })

    return render(request, 'assistant/upload.html')

#delete karnee ke liyeee

def delete_file(request, doc_id):
    try:
        doc = Document.objects.get(id=doc_id)

        # delete physical file
        if os.path.exists(doc.file.path):
            os.remove(doc.file.path)

        # delete faiss + chunks
        index_path = f"media/faiss_{doc.id}.index"
        chunks_path = f"media/chunks_{doc.id}.pkl"

        if os.path.exists(index_path):
            os.remove(index_path)

        if os.path.exists(chunks_path):
            os.remove(chunks_path)

        doc.delete()

        return JsonResponse({"message": "Deleted successfully"})

    except:
        return JsonResponse({"error": "File not found"})
# 💬 Ask Question
def ask_question(request):
    documents = Document.objects.all()

    # 🔥 GET se selected doc (dashboard se aaya)
    selected_doc_id = request.GET.get('doc_id')

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
            return JsonResponse({
                "error": "Index not found. Upload document again."
                })
            #return HttpResponse("Index not found. Upload document again.")

        if not chunks:
            return JsonResponse({
                "error": "No data found for this document"
                })
            #return HttpResponse("No data found for this document ❌")

        # 🔍 Retrieval
        results = search_similar_chunks(query, index, chunks)

        if not results:
            return JsonResponse({
                "error": "No relevant content found"
                })
            #return HttpResponse("No relevant content found ❌")

        # 🤖 Answer
        answer = generate_answer(results, query)

        # 💾 Save history
        ChatHistory.objects.create(
            question=query,
            answer=answer
        )

        return JsonResponse({
            "answer": answer
            })

    # 🔥 GET request (page load)
    return render(request, 'assistant/ask.html', {
        'documents': documents,
        'selected_doc_id': selected_doc_id
    })

# 🕒 Chat History
def history(request):
    chats = ChatHistory.objects.all().order_by('-created_at')

    return render(request, 'assistant/history.html', {
        'chats': chats
    })