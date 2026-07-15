from foundry_local_sdk import Configuration,FoundryLocalManager

MODEL_NAME="phi-4-mini"

config=Configuration(
    app_name="rag-project"
)

FoundryLocalManager.initialize(config)

manager=FoundryLocalManager.instance
model=manager.catalog.get_model(MODEL_NAME)

print("alias:",model.alias)

for variant in model.variants:
    print(
        variant.id,
        "cached:",variant.info.cached
    )





# if not model.is_loaded:
#     print("model is loading...")
#     model.load()

# chat_client=model.get_chat_client()
# print(chat_client)