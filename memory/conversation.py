_history=[]

MAX_HISTORY=4

def add_message(role:str,content:str):
    _history.append(
        {
            "role":role,
            "content":content,
        }
    )
    if len(_history)>MAX_HISTORY*2:
        del _history[:2]

def get_recent_history():
    return _history.copy()

def clear_history():
    _history.clear()


def build_search_query(current_question:str)->str:
    previous_questions=[
       m["content"]
       for m in _history
       if m["role"]=="user"
       ][-2:]

    if len(previous_questions)<=1:
        return current_question

    
    return previous_questions[-2]+ " " + current_question