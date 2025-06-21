import requests
from app.services.llama4_service import rerank_with_llama4, generate_summary

def fetch_books_by_subject(subject: str, limit: int = 20) -> list[dict]:
    subj_key = subject.strip().lower().replace(" ", "_")
    url = f"https://openlibrary.org/subjects/{subj_key}.json?limit={limit}"
    resp = requests.get(url, headers={"User-Agent": "Readio/1.0"})
    if resp.status_code != 200:
        return []
    return resp.json().get("works", [])

def recommend_by_labels(user_labels, top_n=5):
    candidates = []
    for label in user_labels:
        books = fetch_books_by_subject(label)
        for book in books:
            candidates.append({
                'title': book['title'],
                'description': book.get('description', ''),
            })

    # Re-rank candidates using Llama 4
    reranked = rerank_with_llama4(user_labels, candidates)
    return reranked

def generate_video_script(book):
    content = generate_summary(recommend_by_labels(user_labels))
    return f"Discover this amazing book: " + content
