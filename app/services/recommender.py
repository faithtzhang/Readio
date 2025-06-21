import requests
from app.services.llama4_service import rerank_with_llama4
from collections import Counter

def fetch_books_by_subject(subject: str, limit: int = 20) -> list[dict]:
    subj_key = subject.strip().lower().replace(" ", "_")
    url = f"https://openlibrary.org/subjects/{subj_key}.json?limit={limit}"
    resp = requests.get(url, headers={"User-Agent": "Readio/1.0"})
    if resp.status_code != 200:
        return []
    return resp.json().get("works", [])

# def recommend_by_labels_openlib(user_labels: list[str], top_n: int = 5) -> list[dict]:
#     book_counter = Counter()
#     book_info = {}
#     for label in user_labels:
#         works = fetch_books_by_subject(label, limit=20)
#         for w in works:
#             key = w['key']
#             book_counter[key] += 1
#             book_info.setdefault(key, {
#                 'title': w.get('title'),
#                 'authors': [a['name'] for a in w.get('authors', [])],
#                 'cover_id': w.get('cover_id')
#             })
#     results = []
#     for key, score in book_counter.most_common(top_n):
#         info = book_info[key]
#         results.append({
#             'title': info['title'],
#             'authors': info['authors'],
#             'score': score,
#             'cover_url': (
#                 f"https://covers.openlibrary.org/b/id/{info['cover_id']}-L.jpg"
#                 if info.get('cover_id') else None
#             )
#         })
#     return results

def recommend_by_labels(user_labels, top_n=5):
    candidates = []
    for label in user_labels:
        books = fetch_books_by_subject(label)
        for book in books:
            candidates.append({
                'title': book['title'],
                'description': book.get('description', ''),
                'score': 1  # Placeholder score
            })

    # Re-rank candidates using Llama 4
    reranked = rerank_with_llama4(user_labels, candidates)
    return reranked
