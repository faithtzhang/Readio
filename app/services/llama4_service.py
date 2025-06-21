from openai import OpenAI
from app.core.config import LLAMA4_API_BASE, LLAMA4_API_KEY

client = OpenAI(base_url=LLAMA4_API_BASE, api_key=LLAMA4_API_KEY)

# recommend
def rerank_with_llama4(user_labels, candidates):
    prompt = f"User is interested in: {', '.join(user_labels)}.\nCandidates:\n"
    for i, c in enumerate(candidates, 1):
        prompt += f"{i}. {c['title']}: {c.get('description', 'No description')}\n"
    prompt += "Rank them by relevance"

    response = client.chat.ChatCompletion.create(
        model="meta/llama-4-maverick-17b-128e-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512
    )
    return response.choices[0].message.content

# summary
def generate_summary(text: str, voice_style: str) -> str:
    prompt = f"""
    Recommend the following book to user, summarize into a 3-minute audio-ready script.
    Tone: {voice_style}
    ---
    {text}
    """
    response = client.chat.completions.create(
        model="meta/llama-4-maverick-17b-128e-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content

# 3
