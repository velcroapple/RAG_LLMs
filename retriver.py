from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# --- Load Fin-MPNET embedding model ---
model = SentenceTransformer("mukaj/fin-mpnet-base")

# --- Connect to Qdrant server ---
client = QdrantClient(host="localhost", port=6333)

def retrieve_chunks(query, top_k=5):
    # Embed the query
    query_vector = model.encode(query).tolist()

    # Search Qdrant
    results = client.search(
        collection_name="financial_chunks",
        query_vector=query_vector,
        limit=top_k
    )
    chunks = []
    for r in results:
        try:
            chunks.append(r.payload["chunk"])
        except (AttributeError, KeyError, TypeError):
            print(f" Skipped malformed result: {r}")
            continue
    # Return just the chunks
    return chunks
