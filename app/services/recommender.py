from typing import List, Dict

def recommend_by_labels(labels: List[str], top_n: int = 5) -> List[Dict]:
    """Mock recommender service that returns sample recommendations."""
    # Mock recommendations based on labels
    mock_recommendations = [
        {
            "title": "Sample Book 1",
            "author": "Author 1",
            "genre": "fiction",
            "description": "A fascinating story about...",
            "rating": 4.5
        },
        {
            "title": "Sample Book 2", 
            "author": "Author 2",
            "genre": "non-fiction",
            "description": "An insightful analysis of...",
            "rating": 4.2
        },
        {
            "title": "Sample Book 3",
            "author": "Author 3", 
            "genre": "business",
            "description": "Essential strategies for...",
            "rating": 4.7
        }
    ]
    
    # Filter by labels if provided
    if labels:
        filtered_recommendations = []
        for rec in mock_recommendations:
            if any(label.lower() in rec["genre"].lower() for label in labels):
                filtered_recommendations.append(rec)
        return filtered_recommendations[:top_n]
    
    return mock_recommendations[:top_n] 