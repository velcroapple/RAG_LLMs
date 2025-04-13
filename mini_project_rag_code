# Step 1: Install Required Libraries
!pip install -q langchain faiss-cpu pypdf beautifulsoup4 sentence-transformers gradio
!pip install -q langchain_community
!pip install -q ctransformers

# Step 2: Import Dependencies
import requests
from bs4 import BeautifulSoup
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import gradio as gr

# Step 3: Set up Local LLM (instead of HuggingFaceHub)
def get_llm():
    # Download a small model that can run on CPU
    # This uses the llama.cpp implementation via CTransformers
    llm = CTransformers(
        model="TheBloke/Llama-2-7B-Chat-GGML",
        model_file="llama-2-7b-chat.ggmlv3.q4_0.bin",
        config={'max_new_tokens': 256, 'temperature': 0.01}
    )
    return llm

# Step 4: Data Collection Functions
def scrape_ipc_section(section_number, section_id):
    """Scrape IPC sections from Indian Kanoon"""
    try:
        # Use a timeout to avoid getting blocked
        time.sleep(2)
        url = f"https://indiankanoon.org/doc/{section_id}/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        judgment_text = soup.find("div", class_="judgments").text.strip()
        return f"IPC Section {section_number}: {judgment_text}"
    except Exception as e:
        print(f"Error scraping IPC section {section_number}: {e}")
        # Fallback text if scraping fails
        return f"IPC Section {section_number}: This section deals with the Indian Penal Code."

def get_landmark_judgments():
    """Sample landmark judgments"""
    return [
        "Navtej Singh Johar v. Union of India (2018): The Supreme Court held that Section 377 IPC is unconstitutional insofar as it criminalizes consensual sexual conduct between adults of the same sex.",
        "Joseph Shine v. Union of India (2018): The Supreme Court struck down Section 497 IPC which criminalized adultery, holding it to be unconstitutional.",
        "Bachan Singh v. State of Punjab (1980): The Supreme Court established the 'rarest of rare' doctrine for imposing death penalty under Section 302 IPC.",
        "Vishaka v. State of Rajasthan (1997): The Supreme Court defined sexual harassment at the workplace and issued guidelines to prevent it, later codified into law.",
        "K.S. Puttaswamy v. Union of India (2017): The Supreme Court recognized the right to privacy as a fundamental right under Article 21 of the Constitution."
    ]

# Step 5: Collect Data
print("Collecting IPC data...")
ipc_data = {
    "302": scrape_ipc_section(302, "1569253"),  # Murder
    "375": scrape_ipc_section(375, "1649457"),  # Rape
    "376": scrape_ipc_section(376, "2006332"),  # Punishment for rape
    "498A": scrape_ipc_section("498A", "538436"), # Cruelty by husband
    "304B": scrape_ipc_section("304B", "653797")  # Dowry death
}

# Add landmark judgments
judgments = get_landmark_judgments()

# Combine all data
all_texts = list(ipc_data.values()) + judgments
print(f"Collected {len(all_texts)} documents")

# Step 6: Data Preprocessing
print("Preprocessing data...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)

all_chunks = []
for text in all_texts:
    chunks = text_splitter.split_text(text)
    all_chunks.extend(chunks)
print(f"Created {len(all_chunks)} chunks")

# Step 7: Create Vector Database
print("Creating vector database...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_db = FAISS.from_texts(all_chunks, embedding=embeddings)
print("Vector database created")

# Step 8: Set up RAG Pipeline
print("Setting up RAG pipeline...")
llm = get_llm()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_db.as_retriever(search_kwargs={"k": 3})
)
print("RAG pipeline ready")

# Step 9: Create Gradio Interface
def legal_query(query):
    if not query.strip():
        return "Please enter a valid query."
    try:
        result = qa_chain.run(query)
        return result
    except Exception as e:
        return f"Error processing query: {str(e)}"

interface = gr.Interface(
    fn=legal_query,
    inputs=gr.Textbox(lines=2, placeholder="Enter legal query (e.g., 'What is the punishment for murder under IPC?')"),
    outputs="text",
    title="Legal Research Assistant",
    description="Ask questions about Indian Penal Code sections and landmark judgments"
)

# Step 10: Launch Gradio Interface
interface.launch(debug=False)
