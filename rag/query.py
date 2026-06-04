"""
rag/query.py
Tests if ChromaDB is returning correct policy chunks
for a given question
"""

import os
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME    = "ecommerce_policies"

# Load model and connect to ChromaDB
model      = SentenceTransformer("all-MiniLM-L6-v2")
client     = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = client.get_collection(COLLECTION_NAME)


def query_policy(question: str, n_results: int = 3):
    """
    Takes a question
    Returns top matching policy chunks
    """
    print(f"\n🔍 Question: {question}")
    print("-" * 60)

    # Convert question to embedding
    question_embedding = model.encode([question]).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    # Print results
    for i in range(len(results["documents"][0])):
        doc      = results["documents"][0][i]
        source   = results["metadatas"][0][i]["source"]
        distance = results["distances"][0][i]
        score    = round(1 - distance, 4)

        print(f"\n📄 Result {i+1}")
        print(f"   Source:    {source}")
        print(f"   Relevance: {score}")
        print(f"   Text:      {doc[:300]}...")

    return results


# ── Test queries ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("RAG SYSTEM TEST")
    print("=" * 60)

    query_policy("can I return a damaged product?")
    query_policy("how many days do I have to return electronics?")
    query_policy("when will I get my refund after returning?")
    query_policy("what happens if I receive wrong product?")
    query_policy("can I cancel my order after it is shipped?")