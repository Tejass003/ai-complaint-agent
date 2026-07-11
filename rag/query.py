"""
rag/query.py
Query ChromaDB for relevant policy chunks.
Can filter by company for accurate results.
"""

import os
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME    = "ecommerce_policies"

model      = SentenceTransformer("all-MiniLM-L6-v2")
client     = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = client.get_collection(COLLECTION_NAME)

# Map company name to PDF source names
COMPANY_SOURCES = {
    "Amazon":   ["amazon_damaged", "amazon_refund_policy", "amazon_refund_status",
                 "amazon_returns_policy", "amazon_returns_process"],
    "Flipkart": ["flipkart_policy"],
    "Meesho":   ["meesho_returns", "meesho_cancellation"],
}


def query_policy(question: str, n_results: int = 3, company: str = None) -> dict:
    """
    Semantic search over policy chunks.
    If company is provided, only searches that company's policies.
    """
    print(f"\n🔍 Question: {question}")
    if company:
        print(f"   Company filter: {company}")
    print("-" * 60)

    query_embedding = model.encode([question]).tolist()

    # Build company filter if provided
    where_filter = None
    if company and company in COMPANY_SOURCES:
        sources = COMPANY_SOURCES[company]
        if len(sources) == 1:
            where_filter = {"source": {"$eq": sources[0]}}
        else:
            where_filter = {"source": {"$in": sources}}

    # Query ChromaDB
    if where_filter:
        results = collection.query(
            query_embeddings = query_embedding,
            n_results        = n_results,
            where            = where_filter,
            include          = ["documents", "metadatas", "distances"]
        )
    else:
        results = collection.query(
            query_embeddings = query_embedding,
            n_results        = n_results,
            include          = ["documents", "metadatas", "distances"]
        )

    # Print results
    for i in range(len(results["documents"][0])):
        doc    = results["documents"][0][i]
        source = results["metadatas"][0][i]["source"]
        score  = round(1 - results["distances"][0][i], 4)
        print(f"\n📄 Result {i+1}")
        print(f"   Source:    {source}")
        print(f"   Relevance: {score}")
        print(f"   Text:      {doc[:200]}...")

    return results


if __name__ == "__main__":
    print("=== TEST WITHOUT FILTER ===")
    query_policy("can I return a damaged product?")

    print("\n=== TEST WITH AMAZON FILTER ===")
    query_policy("can I return a damaged product?", company="Amazon")

    print("\n=== TEST WITH FLIPKART FILTER ===")
    query_policy("refund for defective electronics", company="Flipkart")