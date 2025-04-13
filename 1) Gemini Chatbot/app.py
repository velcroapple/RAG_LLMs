import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
import json
import os
import faiss
import atexit
import shutil

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

TEMP_DIR = "faiss_index"
EMBEDDINGS_PATH = os.path.join(TEMP_DIR, "embeddings.npy")
DOCS_PATH = os.path.join(TEMP_DIR, "docs.json")

# Clean up on exit
def cleanup():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

atexit.register(cleanup)  # Will run on app exit

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    return splitter.split_text(text)

def get_vectorstore(text_chunks):
    os.makedirs(TEMP_DIR, exist_ok=True)
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    docs = [Document(page_content=chunk, metadata={}) for chunk in text_chunks]

    # Save documents as JSON
    with open(DOCS_PATH, "w") as f:
        json.dump([{"text": doc.page_content, "metadata": doc.metadata} for doc in docs], f)

    # Compute embeddings
    vectors = embeddings_model.embed_documents([doc.page_content for doc in docs])
    np.save(EMBEDDINGS_PATH, np.array(vectors, dtype=np.float32))

def load_vectorstore():
    # Load docs
    with open(DOCS_PATH, "r") as f:
        docs_data = json.load(f)
    docs = [Document(page_content=d["text"], metadata=d["metadata"]) for d in docs_data]

    # Load embeddings
    vectors = np.load(EMBEDDINGS_PATH).astype("float32")

    # Build FAISS index
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    return docs, index

def get_conversation_chain():
    prompt = PromptTemplate(
        template="""
        Answer the question as detailed as possible from the provided context.
        Make sure to provide all the details.
        If the answer is not available in the context, just say "This info is not given in the context" and answer it briefly. 
        start your answer by pritning in bold RAFTAR FORMULA RACING FSG RULES

        Context: \n{context}\n
        Question: \n{question}\n
        Answer:
        """,
        input_variables=["context", "question"]
    )
    # Initialize the model for the Gemini free tier
    model = ChatGoogleGenerativeAI(model="gemini-2.5-pro-exp-03-25", temperature=0.3)

    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def user_input(user_question):
    docs, index = load_vectorstore()
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    query_vector = np.array([embeddings_model.embed_query(user_question)], dtype="float32")

    _, indices = index.search(query_vector, k=5)
    matched_docs = [docs[i] for i in indices[0]]

    chain = get_conversation_chain()
    response = chain({"input_documents": matched_docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply:", response["output_text"])

def main():
    st.set_page_config(page_title="Gemini Chatbot (RAG - PDF)", page_icon=":robot_face:")
    st.header("Ace the rules Quiz with Gemini 🏎️")

    user_question = st.text_input("Enter your question:")
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Document Section:")
        pdf_docs = st.file_uploader("Upload your PDF files here and click 'Submit and Process'", accept_multiple_files=True)
        if st.button("Submit and Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vectorstore(text_chunks)
                st.success("✅ PDFs processed successfully! ✅")

if __name__ == "__main__":
    main()