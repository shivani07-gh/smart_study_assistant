from django.shortcuts import render
from django.http import HttpResponse

from .forms import DocumentForm
from .models import Document
from rag.pdf_loader import extract_text_from_pdf


# Home page
def home(request):
    return HttpResponse("Smart Study Assistant Running 🚀")


# Upload + PDF processing
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save()

            # 📄 PDF path
            file_path = doc.file.path

            # 🧠 Extract text from PDF
            text = extract_text_from_pdf(file_path)

            print("PDF TEXT:\n", text[:1000])  # debug

            return render(request, 'assistant/success.html')

    else:
        form = DocumentForm()

    return render(request, 'assistant/upload.html', {'form': form})