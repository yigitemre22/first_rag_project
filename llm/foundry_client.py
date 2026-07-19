from openai import OpenAI
from llm.foundry_utils import get_foundry_base_url

client=OpenAI(
    base_url=get_foundry_base_url(),
    api_key="foundry"
)

MODEL_NAME="Phi-4-mini-instruct-cuda-gpu:5"

def ask_llm(messages:list[dict])->str:
    
    response=client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=512,
    )

    return response.choices[0].message.content

if __name__=="__main__":
    messages=[
        {
            "role":"user",
            "content":"Merhaba kendini tanıt"
        }
    ]
    answer=ask_llm(messages)

    print(answer)