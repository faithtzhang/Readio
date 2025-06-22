from openai import OpenAI
from app.config import settings

client = OpenAI(base_url="https://api.llama.com/compat/v1/", api_key=settings.LLAMA4_API_KEY)

# recommend
def rerank_with_llama4(user_labels, candidates):
    prompt = f"User is interested in: {', '.join(user_labels)}.\nCandidates:\n"
    for i, c in enumerate(candidates, 1):
        prompt += f"{i}. {c['title']}: {c.get('description', 'No description')}\n"
    prompt += "Pick the best choice, return book name and author"

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""

# text summary
def generate_summary(text: str, voice_style: str = "Neutral") -> str:
    prompt = f"""
    Recommend the following book to user, summarize into a 9-second audio-ready script. Only return the summarized content.
    Tone: {voice_style}
    ---
    {text}
    """
    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return response.choices[0].message.content or ""

# video explain
def summarize_video_with_frames(frame_urls: list[str], duration, perspective: str) -> str:
    content = (
        "Here is the perspective setting: \n" + perspective + "\n\n"
        "And here are key frames (as URLs):\n" +
        "\n".join(frame_urls) +
        "\n\nPlease imagine the video based on the frames of it, then generate a narration for the video, do not exceed video length (" + 
        str(duration) + " frames). Only return description content."
    )
    resp = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": content}],
        max_tokens=150
    )
    return resp.choices[0].message.content.strip()

