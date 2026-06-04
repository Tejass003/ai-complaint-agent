"""
rag/ingest.py
Reads all PDFs from data/ folder
Splits into chunks
Generates embeddings
Stores in ChromaDB
"""

import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

load_dotenv()

# ── Settings ──────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
POLICY_PDF_PATH    = os.getenv("POLICY_PDF_PATH", "./data/")
COLLECTION_NAME    = "ecommerce_policies"
CHUNK_SIZE         = 500   # characters per chunk
CHUNK_OVERLAP      = 100   # overlap between chunks

# ── Step 1: Load embedding model ──────────────────────────────────────
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded")

# ── Step 2: Connect to ChromaDB ───────────────────────────────────────
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
client     = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# ── Step 3: Extract text from a single PDF ────────────────────────────
def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text   = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


# ── Step 4: Split text into overlapping chunks ────────────────────────
def split_into_chunks(text: str, source: str) -> list:
    chunks = []
    start  = 0
    index  = 0

    while start < len(text):
        end   = start + CHUNK_SIZE
        chunk = text[start:end]

        if chunk.strip():
            chunks.append({
                "id":     f"{source}_chunk_{index}",
                "text":   chunk.strip(),
                "source": source
            })
            index += 1

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# ── Step 5: Ingest all PDFs ───────────────────────────────────────────
def ingest_all_pdfs():
    # Check if already ingested
    if collection.count() > 0:
        print(f"✅ ChromaDB already has {collection.count()} chunks — skipping")
        return

    pdf_files = [f for f in os.listdir(POLICY_PDF_PATH) if f.endswith(".pdf")]

    if not pdf_files:
        print("❌ No PDF files found in data/ folder")
        return

    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")

    all_chunks = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(POLICY_PDF_PATH, pdf_file)
        source   = pdf_file.replace(".pdf", "")

        print(f"  Reading: {pdf_file}")
        text   = extract_text_from_pdf(pdf_path)
        chunks = split_into_chunks(text, source)
        all_chunks.extend(chunks)
        print(f"  → {len(chunks)} chunks created")

    print(f"\nGenerating embeddings for {len(all_chunks)} chunks...")
    texts      = [c["text"]   for c in all_chunks]
    ids        = [c["id"]     for c in all_chunks]
    metadatas  = [{"source": c["source"]} for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # Store in ChromaDB
    collection.upsert(
        ids        = ids,
        documents  = texts,
        embeddings = embeddings,
        metadatas  = metadatas
    )

    print(f"\n✅ Done! {len(all_chunks)} chunks stored in ChromaDB")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Location:   {CHROMA_PERSIST_DIR}")


if __name__ == "__main__":
    ingest_all_pdfs()