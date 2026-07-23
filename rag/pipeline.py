from retriever.search import search_documents
from llm.foundry_client import ask_llm
from memory.chat_memory import(
    add_message,
    get_history
)
from memory.chat_memory import clear_history
from memory.conversation import(
    add_message,
    get_recent_history,
    build_search_query,
)
def answer_question(
        question:str,
        filename:str |None=None,
    ):
    add_message(
        "user",
        question,
    )
    search_query=build_search_query()
    print(f"\nSearch Query: {search_query}")
    documents=search_documents(search_query)

    context="\n\n".join(
                row[4] for row in documents
    )

    history="\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in get_recent_history()
    )

    prompt = f"""
                You are a Retrieval-Augmented Generation (RAG) assistant.

                Conversation History:
                {history}

                Retrieved Context:
                {context}

                Current Question:
                {question}

                Rules:
                - Answer ONLY using the Retrieved Context.
                - Use the Conversation History only to understand references such as "it", "its advantages", "that topic", etc.
                - Never use your own knowledge.
                - Never guess.
                - If the answer is not explicitly present in the Retrieved Context, reply exactly:

                I don't know.

                Answer:
                """
    
    messages=[]

    messages.extend(get_history())

    messages.append(
        {
            "role":"user",
            "content":prompt,
        }
    )


    answer=ask_llm(messages)

    add_message("assistant",answer)
   
    return answer,documents 

if __name__=="__main__":
    while True:

        question=input("\nQuestion:")

        if question.lower()=="exit":
            clear_history()
            break

        answer,documents=answer_question(question)
        print(get_recent_history())
        print("\nAnswer:\n")
        print(answer)

        print("\n"+"="*60)
        print("sources")
        print("="*60)

        for doc in documents:
            print(
                f"- {doc[1]} |"
                f"Page: {doc[2]} |"
                f"Chunk: {doc[3]} |"
                f"Distance: {doc[5]:.4f}"
            )