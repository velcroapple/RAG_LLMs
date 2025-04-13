# KG_RAG_HVAC_AI_Club_DC_Project
This repository contains the project work done by Aishwarya Ajit Abhyankar during the tenure of Deputy Coordinator in AI club (2024-25).
# 🧠 Neo4j + Ollama RAG Chatbot

This project connects a Neo4j knowledge graph with a local CPU-friendly LLM (like Mistral via Ollama) to answer natural language queries using Retrieval-Augmented Generation (RAG).
The knowledge graph is created from data obtained from abstracts of HVAC(Heating, Ventilation, Air Conditioning) patents on https://patents.justia.com.

## Inspiration 

- The research paper here : https://www.sciencedirect.com/science/article/pii/S095070512401044X was the main inspiration for this project. The methodology used is almost the same. Only the exact models used are different.
- The research paper's authors have developed a fine tuned version of albert/albert-large-v2 for identifying specific triples in scientific text(patent descriptions).
- This project uses different, simpler models for the same purpose.
- The triplets are of the form 'head', 'tail', 'relationship'.

## Process 

- Web scraping to collect data
- Converting text to triplets - using spacy and the model Babelscape/rebel-large
- Loading the triplet data to a Neo4j knowledge graph
- Retrieving relevant context to the query from the graph using Cypher queries
- Sending context + user query to a local LLM(Mistral)
- Generating human-like answers using the LangChain framework
- Presenting a friendly UI for querying

## Files

- The code can be found in all_other_code.ipynb
- The scraped data is in justia_patents.csv
- The triplets are in justia_triplets_all.csv
- The cleaned triplets are in cleaned_triplets.csv
- The knowledge graph is available in csv form as knowledge_graph.csv
- The patents_knowledge_graph.png can be viewed for visualizing the graph
- The RAG based chatbot is included in the notebook all_other_code.ipynb
- Examples of queries and responses are uploaded as example.png 

## Dependencies/built with
- py2neo
- langchain
- gradio
- ollama
- Neo4j

