from retriver import retrieve_chunks
from subquerry import split_query

# chunks = retrieve_chunks("Net Profit from Quarterly results of Dr Reddy Laboratory Ltd for Sep 2023?")
# for i, chunk in enumerate(chunks, 1):
#     print(f"\n--- Chunk {i} ---\n{chunk}")


user_query = "What is total of last 3 quater sales of grasim industries?"


# print(" Subqueries:")
# for q in subqueries:
#     print("-", q)


def retrieve_chunks_multi(user_query: str, top_k_per_subquery=3) -> list[str]:
    # Step 1: Split into subqueries
    subqueries = split_query(user_query)
    # print(f" Subqueries:\n- " + "\n- ".join(subqueries))

    # Step 2: Retrieve chunks per subquery
    all_chunks = []
    seen = set()

    for subquery in subqueries:
        chunks = retrieve_chunks(subquery, top_k=top_k_per_subquery)
        for chunk in chunks:
            if chunk not in seen:
                all_chunks.append(chunk)
                seen.add(chunk)

    print(f"\n Retrieved {len(all_chunks)} unique chunks from {len(subqueries)} subqueries.")
    
    return all_chunks

def build_prompt(user_query: str, subqueries: list[str], chunks: list[str]) -> str:
    subquery_section = "\n".join(subqueries)
    context_section = "\n\n".join(chunks)

    return f"""
You are a financial analysis assistant built on top of structured financial data from Screener-like Excel tables.

You will be given:
- The original user query
- Subqueries generated to help retrieve relevant data
- A list of text chunks (retrieved context)

Use only the information present in the chunks to answer the question. Do not use your own knowledge or assumptions. If the answer is not possible with the given data, politely say you cannot help.

---

User Query:
{user_query}

Subqueries:
{subquery_section}

Chunks:
{context_section}

---

Instructions:
- Answer only what the user has asked.
- Do not go beyond what the user is asking.
- If the question involves a derived metric (like average, sum, growth), compute it based on values found in the chunks.
- If a component metric is not explicitly labeled (e.g. "Revenue"), but a similar field like "Sales" is found, you may use that as a substitute (e.g. treat Sales as Revenue when computing Profit Margin).
- Never mention a company that does not appear in the retrieved chunks, even if it was indirectly referred to.
- If the query is outside the domain of financial analysis (e.g. "what is the national bird of India"), say: "I'm a financial assistant and cannot answer non-finance questions."
- If the user message is casual or off-topic (like "hi", "yo", "how are you", etc), respond with: "I'm a financial assistant. Try asking me about ROE, EPS, Revenue, or anything finance-related."


Now generate the answer, clearly and concisely, using only the facts present in the chunks.
""".strip()

import requests



def ask(user_query: str, top_k=3) -> str:
    # print(" Splitting query...")
    subqueries = split_query(user_query)
    # If subquery itself is a denial or casual reply → skip the pipeline
    if isinstance(subqueries, list) and len(subqueries) == 1:
        first = subqueries[0].strip().lower()
        if first.startswith("i'm a financial assistant") or first.startswith("sorry"):
            return subqueries[0]

    # print(" Retrieving chunks...")
    chunks = retrieve_chunks_multi(user_query, top_k_per_subquery=top_k)

    # print(" Building prompt...")
    prompt = build_prompt(user_query, subqueries, chunks)

    print(" Sending to Mistral (via Ollama)...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return f" LLM error: {response.status_code}\n{response.text}"
answer = ask("Hi")
print(answer)
