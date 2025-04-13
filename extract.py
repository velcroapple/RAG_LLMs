import requests
from bs4 import BeautifulSoup as bs
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.html import HTMLSectionSplitter
import json

import time
import re
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random

BASE_URL = "https://dune.fandom.com"

#a session is just sending a request to accesss the content of the url.
def get_session():
    session = requests.Session()
	#requests.session instead of requests.get to use the same connection for the consequent connections 
    retry = Retry(
        total=5,
        backoff_factor=1,
		#backoff factor so that we don't hammer it with multiple retries
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Function to extract content from an article URL
def extract_article_content(url):
    session = get_session()
    response = session.get(url, timeout=10)
    if response.status_code != 200:
        print(f"Skipping {url} due to status {response.status_code}")
        return ""
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    #ADDED: Extract title from URL and add it to metadata 
    title = url.split('/')[-1].replace('_', ' ')
    for doc in docs:
        doc.metadata["Title"] = title  #because of some inconsistency in the parser and webbaseloader
    
    headers_to_split = [("h1", "Header 1"), ("h2", "Header 2"), ("h3", "Header 3"), ("h4", "Header 4")]
    html_splitter = HTMLSectionSplitter(headers_to_split)
    html_header_splits = html_splitter.split_documents(docs)
	#chunking
    chunk_size = 700
    chunk_overlap = 70
    rec_char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap)
    
    final_splits = rec_char_splitter.split_documents(html_header_splits)
    return final_splits


def main():
    i=0
        # Get all article URLs
    with open(r"[ARTICLE_LINKS.JSON_PATH]", 'r') as f:
        article_urls = json.load(f)
        
    
    all_documents = []  
    
    for url in list(article_urls):
        documents = extract_article_content(url)  
        all_documents.extend(documents)  
        print(i)
        i+=1

    #Convert Document objects to dictionaries for JSON serialization
    doc_data = []
    for doc in all_documents:
        # Clean up the page content
        cleaned_content = doc.page_content
        cleaned_content = re.sub(r'\n+', '\n', cleaned_content)
        cleaned_content = re.sub(r'\t+', ' ', cleaned_content)
        cleaned_content = re.sub(r' +', ' ', cleaned_content)
        cleaned_content = cleaned_content.strip()
    
        doc_data.append({
            "page_content": cleaned_content,
            "metadata": doc.metadata
        })
    with open('data.json', 'w') as f:
        json.dump(doc_data, f)
    

if __name__ == "__main__":
    main()
