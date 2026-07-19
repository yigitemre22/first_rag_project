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


def build_search_query()->str:
    questions=[
       m["content"]
       for m in _history
       if m["role"]=="user"
       ]

    
    return " ".join(questions[-3:])