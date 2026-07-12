from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts:list[str])->list[list[float]]:
    if not texts:
        raise ValueError("texts lists cannot be empty")

    if any(not text.strip() for text in texts):
        raise ValueError("text lists cannot contain empty strings")

    embeddings=model.encode(texts)
    return embeddings.tolist()

if __name__=="__main__":
    sample_texts = [
    "Bellek işletim sisteminin önemli bir parçasıdır.",
    "CPU işlemleri sırayla yürütür.",
    "Python popüler bir programlama dilidir."
]
    embeddings=generate_embeddings(sample_texts)
    print(len(embeddings))
    print(len(embeddings[0]))