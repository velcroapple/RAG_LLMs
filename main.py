import os
import pickle
import streamlit as st
import numpy as np
import faiss
from langchain_community.embeddings import HuggingFaceEmbeddings
#we'll use all-MiniLM-L6-v2
from langchain_core.documents import Document
from langchain_ollama.llms import OllamaLLM
from sentence_transformers import SentenceTransformer

BASE_URL = "https://dune.fandom.com"

#FAISS is used for similarity search. it stores the vectors and associated index.
index = faiss.read_index(r"C:\Users\avish\RAG\faiss_index.index")

#the retrieved vectors' indices correspond to their metadata here
with open(r"C:\Users\avish\RAG\faiss_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


import requests
import google.generativeai as genai
import os

#you first have to set up an env variable for your api key
genai.configure(api_key=os.environ["MYKEY"])

model = genai.GenerativeModel("gemini-1.5-pro")

def generate_answer(query, context_docs):
    if not context_docs:
        return "I couldn't find anything relevant in the Dune Wiki."
		
    #truncating because it might exceed the llm's input token limit
    context = "\n".join(doc[0:300] for doc in context_docs)
    
    prompt = f"""Answer this question using ONLY the context below. Answer in about sixty words.\n
    Context:\n{context}\n\n
    Question: {query}
    """
    response = model.generate_content(prompt)
    return response.text

embedder = SentenceTransformer("all-MiniLM-L6-v2")
#the same one we used for vector embeddings 

def main():

    st.title("Dune AI RAG Chatbot")
    st.write(f"Welcome to the Dune wiki chatbot!")
    
    query = st.text_input("Ask something:")

    if query:
        st.write("Searching...")
        query_vector = embedder.encode([query])
        query_vector = np.array(query_vector).astype("float32")

        k = 3
        _, indices = index.search(query_vector, k)

        retrieved_docs = [metadata[i] for i in indices[0]]
    
        answer = generate_answer(query, retrieved_docs)
        st.write(answer)
      

if __name__ == "__main__":
    main()
