from sentence_transformers import CrossEncoder

reranker=CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank(query,documents,top_k=5):

    pairs=[
        (query,row[4])
        for row in documents
    ]

    scores=reranker.predict(pairs)

    ranked=sorted(
        zip(scores,documents),
        key=lambda x:x[0],
        reverse=True,
    )

    return[
        doc
        for score,doc in ranked[:top_k]
    ]