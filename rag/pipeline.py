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
    try:
        add_message(
            "user",
            question,
        )
        search_query=build_search_query(question)
        print(f"\nSearch Query: {search_query}")
        documents=search_documents(search_query,filename=filename)

        print("=" * 60)
        print("Retrieved Documents")
        print("=" * 60)

        for d in documents:
            print(f"{d[1]} | Page {d[2]} | Score {d[5]:.4f}")
        
        if not documents:
            add_message(
                "assistant",
                "I don't know."
            )
            return "I don't know", []

        context="\n\n".join(
                    row[4][:500] for row in documents
        )

        print("=" * 80)
        print(context)
        print("=" * 80)

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

                    - Answer ONLY from the Retrieved Context.
                    - Do NOT use your own knowledge.
                    - Do NOT invent information.
                    - Do NOT add suggestions.
                    - Do NOT explain beyond the retrieved text.
                    - If the answer is incomplete in the context, answer only with the available information.
                   If the retrieved context is related to the question but does not containan explicit definition, explain what is available in the retrieved context.
                    
                    Only answer "I don't know." if the retrieved context is completely unrelated.

                    Write the answer in Turkish.
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

    except Exception as e:
        print(f"[Pipeline Error] {e}")
        raise

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