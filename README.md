# 📚 Smart Study Assistant (AI-Powered RAG System)

An AI-powered study assistant that allows users to upload PDF documents and ask questions based on their content using a Retrieval-Augmented Generation (RAG) approach.

---

## 🚀 Overview

Smart Study Assistant helps users quickly understand their study material by answering questions directly from uploaded PDFs.
Instead of reading long documents, users can interact with them and get relevant answers instantly.

---

## ✨ Features

* 📄 Upload PDF documents
* 🔍 Extract text (supports scanned PDFs using OCR)
* ✂️ Split content into smaller parts
* 🔎 Retrieve relevant information
* 💬 Ask questions and get AI-generated answers
* 🧠 Context-based response generation
* 🗂 Chat history tracking
* 🧹 Delete documents with cleanup
* 🎯 Clean and user-friendly interface

---

## 🏗 Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **AI Model:** LLaMA 3.1 (via NVIDIA API)
* **Vector Search:** FAISS
* **Embeddings:** Sentence Transformers
* **Processing:** PDF extraction + OCR

---

## 🎥 Demo

👉 Click below to watch the project demo:

[![Smart Study Assistant Demo](https://img.youtube.com/vi/FmDKUYzhB28/0.jpg)](https://www.youtube.com/watch?v=FmDKUYzhB28)

---

## 📸 Screenshots

### 🔐 Login Page
<p align="left">
<img width="700" alt="login" src="https://github.com/user-attachments/assets/88f17ce7-5c0c-47e2-81d2-5cdd2149ccf8" />
</p>

### 📊 Dashboard
<p align="center">
  <img width="700" alt="dashboard" src="https://github.com/user-attachments/assets/14981578-5af5-4ab9-bbe5-6d5bd1c7a211" />
</p>

### 📤 Upload Page
<p align="center">
<img width="700" alt="upload" src="https://github.com/user-attachments/assets/f9a16b38-59c8-4f8e-8f5b-a1afdf386392" />
</p>

### 💬 Chat Interface
<p align="center">
<img width="700" alt="chat" src="https://github.com/user-attachments/assets/225bf021-b1d7-4716-8bc0-3413ccb38ab0" />
</p>

### 📜 History Page
<p align="center">
<img width="700" alt="history" src="https://github.com/user-attachments/assets/7b1b867b-a155-4f02-9866-094a289e8338" />
</p>
---

## ⚙️ How It Works

1. Upload a PDF
2. Text is extracted from the document
3. Content is split into smaller chunks
4. Each chunk is converted into embeddings
5. Data is stored for fast searching
6. When a user asks a question:

   * Relevant parts are retrieved
   * Passed to the AI model
   * Final answer is generated

---

## 📁 Project Structure

```bash id="1p7m2d"
smart_study_assistant/
│
├── assistant/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│
├── rag/
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── retrieval.py
│   ├── generator.py
│
├── media/
├── manage.py
└── db.sqlite3
```

---

## 🔧 Setup Instructions

### 1. Clone Repository

```bash id="r3x2lm"
git clone https://github.com/shivani07-gh/smart_study_assistant.git
cd smart_study_assistant
```

### 2. Create Virtual Environment

```bash id="n8q2vk"
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash id="9x6t4r"
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file:

```env id="y5m8hz"
NVIDIA_API_KEY=your_api_key_here
```

### 5. Run Server

```bash id="2z0q1c"
python manage.py migrate
python manage.py runserver
```

---

## 🌐 Usage

* `/upload/` → Upload PDF
* `/chat/` → Ask questions
* Select document → Get answers

---

## 🚀 Future Improvements

* Real-time streaming responses
* Highlight answers from documents
* Multi-document support
* Cloud deployment
* User authentication

---

## 👩‍💻 Author

**Shivani Barot**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
