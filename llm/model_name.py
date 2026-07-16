from foundry_local_sdk import Configuration, FoundryLocalManager
import inspect

FoundryLocalManager.initialize(
    Configuration(
        app_name="rag-project",
        model_cache_dir=r"C:\Users\yigit\.foundry\cache\models"
    )
)

manager = FoundryLocalManager.instance

model = manager.catalog.get_model("phi-4-mini")

print(model.variants)
for variant in model.variants:
    print("=" * 50)
    print("ID:", variant.id)
    print("Cached:", variant.info.cached)
    print(dir(variant.info))
    print(inspect.signature(model.select_variant))