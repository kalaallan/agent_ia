import os
import uuid
import chromadb
import fitz
import pytesseract

from pdf2image import convert_from_path
from llama_index.core import Document, StorageContext, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

UPLOAD_DIR = "uploads"
INDEX_DIR = "chroma_db"

os.makedirs(UPLOAD_DIR, exist_ok=True)

Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

chroma_client = chromadb.PersistentClient(path=INDEX_DIR)
chroma_collection = chroma_client.get_or_create_collection("pdf_chunks")


# ---------- CLEAN TEXT ----------
def clean_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\x00", " ").split())


# ---------- OCR ----------
def ocr_page(pdf_path: str, page_number: int) -> str:
    images = convert_from_path(
        pdf_path,
        first_page=page_number + 1,
        last_page=page_number + 1
    )

    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"

    return text


# ---------- PAGE EXTRACTION ----------
def extract_pdf_pages(pdf_path: str):
    doc = fitz.open(pdf_path)

    pages_data = []

    for i, page in enumerate(doc):
        text = page.get_text()
        text = clean_text(text)

        if len(text) < 30:
            print(f"OCR page {i}")
            text = clean_text(ocr_page(pdf_path, i))

        images = []
        for img in page.get_images(full=True):
            images.append(img[0])  # xref uniquement pour identifier l'image

        pages_data.append({
            "page": i,
            "text": text,
            "images": images
        })

    return pages_data


def handle_upload(file_bytes: bytes) -> str:

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    pages = extract_pdf_pages(file_path)

    documents = []

    for page in pages:
        if not page["text"].strip():
            continue

        documents.append(
            Document(
                text=page["text"],
                metadata={
                    "file_id": file_id,
                    "page": page["page"],
                    "has_images": len(page["images"]) > 0
                }
            )
        )

    for doc in documents:
        print("=== DOCUMENT ===")
        print("META:", doc.metadata)
        print("TEXT:", doc.text[:1000])

    if not documents:
        raise ValueError("Aucun contenu exploitable dans le PDF")

    vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

    return file_id