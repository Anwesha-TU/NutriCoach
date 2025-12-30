import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai


genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
BASE_DIR = os.path.dirname(__file__)
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "embeddings.json")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# client = genai.Client()  # uses GEMINI_API_KEY from environment


with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
    INGREDIENTS = json.load(f)


def cosine_similarity(a, b):
    dot_prod = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_prod / (norm_a * norm_b)

def retrieve(query, ingredients, k=3):
    query_emb = model.encode(query)
    scores = []
    for ing in ingredients:
        score = cosine_similarity(query_emb, np.array(ing["embedding"]))
        scores.append((score, ing))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [ing for _, ing in scores[:k]]

def build_context(retrieved):
    return "\n".join(
        f"{r['name']} → {r['evidence_strength']} evidence; "
        f"{', '.join(r['health_concern_type']).lower()}"
        for r in retrieved
    )

#Main entry


def run_model(user_query):
    # model = genai.GenerativeModel("gemini-2.5-flash")
    retrieved = retrieve(user_query, INGREDIENTS, k=3)

    if not retrieved:
        return {
            "summary": "There is very limited information available for these ingredients.",
            "details": "The ingredient label does not provide enough evidence-backed insights.",
            "uncertainty": "Effects may vary depending on formulation and consumption frequency."
        }

    context = build_context(retrieved)

    prompt = f"""
You are an expert AI health co-pilot helping consumers make sense of food ingredients.

Rules:
- Do not make absolute disease claims
- Do not repeat ingredient names
- Use simple English
- Explain tradeoffs
- Consider uncertainty
- Answer only using the context
- Keep it short

Ingredient insights:
{context}

Respond exactly in this format:

Summary:
Details:
Uncertainty:
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    text = response.text.strip()

    sections = {"summary": "", "details": "", "uncertainty": ""}
    current = None

    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Summary:"):
            current = "summary"
            sections[current] = line.replace("Summary:", "").strip()
        elif line.startswith("Details:"):
            current = "details"
            sections[current] = line.replace("Details:", "").strip()
        elif line.startswith("Uncertainty:"):
            current = "uncertainty"
            sections[current] = line.replace("Uncertainty:", "").strip()
        elif current:
            sections[current] += " " + line

    return sections
