from openai import OpenAI
from app.core.config import LLAMA4_API_KEY

# Create client lazily to avoid import-time errors
_client = None

def get_client():
    """Get the OpenAI client, creating it if necessary."""
    global _client
    if _client is None:
        if not LLAMA4_API_KEY:
            raise ValueError("LLAMA4_API_KEY environment variable is not set")
        _client = OpenAI(base_url="https://api.llama.com/compat/v1/", api_key=LLAMA4_API_KEY)
    return _client

# recommend
def rerank_with_llama4(user_labels, candidates):
    client = get_client()
    prompt = f"User is interested in: {', '.join(user_labels)}.\nCandidates:\n"
    for i, c in enumerate(candidates, 1):
        prompt += f"{i}. {c['title']}: {c.get('description', 'No description')}\n"
    prompt += "Pick the best choice, return book name and author"

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""

# summary
def generate_summary(text: str) -> str:
    client = get_client()
    prompt = f"""
    Recommend the following book to user, summarize into a 3-minute audio-ready script.
    ---
    {text}
    """
    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""

# 3
