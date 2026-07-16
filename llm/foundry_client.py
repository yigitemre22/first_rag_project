from openai import OpenAI

client=OpenAI(
    base_url="http://127.0.0.1:60563/v1",
    api_key="foundry"
)

MODEL_NAME="Phi-4-mini-instruct-cuda-gpu:5"

def ask_llm(prompt:str)->str:
    response=client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{
            "role":"user",
            "content":prompt
        }],
        temperature=0.2,
        max_tokens=512
    )
    return response.choices[0].message.content

if __name__=="__main__":
    answer=ask_llm("merhaba kendini tanıt")
    print(answer)