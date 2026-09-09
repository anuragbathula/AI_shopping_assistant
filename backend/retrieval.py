"""Small local retrieval adapter for non-transactional help content.

In production this adapter can be replaced by a vector-store retriever. It returns
only matching public support documents, never inferred facts.
"""
DOCUMENTS = [
    {"terms": ("track", "tracking", "order"), "text": "To check an order, send the order number. I can then look up the latest available status."},
    {"terms": ("return", "returns"), "text": "I do not have a matching support document for returns in this demo. Please contact customer support for return help."},
]


def retrieve(query: str) -> list[str]:
    query_terms = set(query.casefold().split())
    return [document["text"] for document in DOCUMENTS if query_terms.intersection(document["terms"])]
