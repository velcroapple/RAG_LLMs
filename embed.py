from sentence_transformers import SentenceTransformer
import numpy as np
import json
import re
import pickle
import faiss

#text cleaning (removing the footers)
def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"Follow Us.*?Join Fan L", "", text, flags=re.DOTALL)
    return text.strip()

# Load data from data.json 
with open(r"[DATA.JSON_PATH]", "r") as f:
    articles_data = json.load(f)

# Convert JSON data into a list of texts (you could also store metadata separately)
texts = [clean_text(article["page_content"]) for article in articles_data]
print(f"Loaded {len(texts)} documents.")

# simple embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
batch_size = 64
embeddings_list = []

for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i+batch_size]
    batch_embeddings = model.encode(batch_texts, show_progress_bar=False)
    embeddings_list.append(batch_embeddings)
    print(i)

# Concatenate all batch embeddings into one array
embeddings = np.vstack(embeddings_list)

# Build a FAISS index using distance
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings.astype("float32"))
faiss.write_index(index, "faiss_index.index")


# Save the texts as metadata for later retrieval
with open("faiss_metadata.pkl", "wb") as f:
    pickle.dump(texts, f)
print("Metadata saved as 'faiss_metadata.pkl'.")
