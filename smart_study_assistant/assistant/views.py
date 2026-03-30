from django.shortcuts import render
from django.http import HttpResponse

from .forms import DocumentForm
from .models import Document
from rag.pdf_loader import extract_text_from_pdf
from rag.chunking import chunk_text


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
            else:
                print("⚠️ No chunks generated")

            return render(request, 'assistant/success.html')

    else:
        form = DocumentForm()

    return render(request, 'assistant/upload.html', {'form': form})