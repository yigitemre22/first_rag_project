from openai import OpenAI

client=OpenAI(
    base_url="http://127.0.0.1:49268/v1",
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