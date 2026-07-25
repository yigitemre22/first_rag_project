from foundry_local_sdk import Configuration
from foundry_local_sdk import FoundryLocalManager
from foundry_local_sdk.exception import FoundryLocalException
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
    try:
        response=embedding_client.generate_embedding(text)
        return response.data[0].embedding

    except FoundryLocalException as e:
        print(f"[Embedding Error] {e}")
        raise

    except Exception as e:
        print(f"[Unexpected Error] {e}")
        raise

def generate_embeddings(texts:list[str]):
    try:
        response=embedding_client.generate_embeddings(texts)
        return [item.embedding for item in response.data]

    except FoundryLocalException as e:
        print(f"[Embedding Error] {e}")
        raise

    except Exception as e:
        print(f"[Unexpected error] {e}")
        raise

if __name__=="__main__":
    emb=generate_embedding("hello world")

    print(len(emb))
    print(emb[:10])