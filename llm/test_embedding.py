from foundry_local_sdk.configuration import Configuration
from foundry_local_sdk.foundry_local_manager import FoundryLocalManager

FoundryLocalManager.initialize(
    Configuration(app_name="rag-project")
)

manager = FoundryLocalManager.instance

model = manager.catalog.get_model("qwen3-embedding-0.6b")

print("Cached:", model.is_cached)
print("Loaded:", model.is_loaded)

if not model.is_loaded:
    print("Loading model...")
    model.load()

embedding_client = model.get_embedding_client()

result = embedding_client.generate_embedding(
    "Merhaba dünya"
)

print(result)
print(type(result))
print(dir(result))

vector = result.data[0].embedding

print(len(vector))
print(vector[:10])
