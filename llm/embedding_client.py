from foundry_local_sdk import Configuration
from foundry_local_sdk import FoundryLocalManager

FoundryLocalManager.initialize(
    Configuration(
        app_name="rag-project"
    )
)
manager=FoundryLocalManager.instance

model=manager.catalog.get_model("qwen3-embedding-0.6b")

if not model.is_loaded:
    print("loading embedding model")
    model.load()

embedding_client=model.get_embedding_client()

def generate_embedding(text:str):
    response=embedding_client.generate_embedding(text)
    return response.data[0].embedding

def generate_embeddings(texts:list[str]):
    response=embedding_client.generate_embeddings(texts)
    return [item.embedding for item in response.data]

if __name__=="__main__":
    emb=generate_embedding("hello world")

    print(len(emb))
    print(emb[:10])