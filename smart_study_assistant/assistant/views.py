from django.shortcuts import render
from django.http import HttpResponse

from .forms import DocumentForm
from .models import Document
from rag.pdf_loader import extract_text_from_pdf
from rag.chunking import chunk_text
from rag.embeddings import create_embeddings, store_in_faiss


# Home page
def home(request):
    return HttpResponse("Smart Study Assistant Running 🚀")


# Upload + PDF processing
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save()

            file_path = doc.file.path

            text = extract_text_from_pdf(file_path)

            print("TEXT LENGTH:", len(text))   # 👈 add this

            chunks = chunk_text(text)

            print("TOTAL CHUNKS:", len(chunks))   # 👈 add this

            # 👇 SAFE CHECK (IMPORTANT)
            if len(chunks) > 0:
                print("FIRST CHUNK:\n", chunks[0])

                embeddings = create_embeddings(chunks)
                print("EMBEDDINGS SHAPE:", embeddings.shape)
                index = store_in_faiss(embeddings)

            else:
                print("⚠️ No chunks generated")

            return render(request, 'assistant/success.html')
        chunks = chunk_text(text)


    else:
        form = DocumentForm()

    return render(request, 'assistant/upload.html', {'form': form})