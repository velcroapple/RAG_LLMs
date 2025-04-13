import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

# --- Connect to Qdrant ---
client = QdrantClient(host="localhost", port=6333)
collection_name = "financial_chunks"

# --- Recreate collection ---
if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# --- Load your full Qdrant-style points directly ---
points = []

with open("qdrant_chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        points.append(PointStruct(
            id=str(uuid4()),             # fresh UUID
            vector=obj["vector"],        # already in place
            payload=obj["payload"]       # payload is already built!
        ))

# --- Upload to Qdrant ---
client.upload_points(collection_name=collection_name, points=points)
print(f" Uploaded {len(points)} chunks into '{collection_name}' on localhost:6333")
