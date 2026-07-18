from retriever.search import search_documents
from llm.foundry_client import ask_llm

def answer_question(question:str)->str:
    documents=search_documents(question)

    context="\n\n".join(
                row[2] for row in documents
    )

    prompt = f"""
            You are an AI assistant.

            Answer ONLY using the context below.

            If the answer is not in the context, say:

            "I don't know."

            Context:

            {context}

            Question:

            {question}

            Answer:
            """
    
    messages=[
        {
            "role":"user",
            "content":prompt,
        }
    ]
    return ask_llm(messages)

if __name__=="__main__":
    while True:

        question=input("\nQuestion:")

        if question.lower()=="exit":
            break

        answer=answer_question(question)

        print("\nAnswer:\n")
        print(answer)