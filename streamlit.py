import streamlit as st
from app import ask  # Make sure this points to your main `ask()` function

# --- Streamlit Page Settings ---
st.set_page_config(page_title="📊 Financial RAG Chatbot", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    body {
        background-color: #f8f9fb;
    }
    .stTextInput > div > div > input {
        padding: 0.8rem;
        font-size: 16px;
    }
    .response-box {
        background-color: #ffffff;
        padding: 1.2rem;
        margin-top: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.image("https://img.icons8.com/color/96/graph.png", width=60)
st.title("Financial RAG Chatbot")
st.markdown("Ask any financial question from Screener-style data.")

# --- Input ---
user_query = st.text_input("Your Question", placeholder="e.g. What is ROE of Infosys in 2024?")

if st.button("Get Answer") or user_query:
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                final_answer = ask(user_query)
                st.markdown(f"<div class='response-box'>{final_answer}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
