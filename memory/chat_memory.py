MAX_HISTORY=10

_history=[]

def add_message(role:str,content:str):
    _history.append(
        {
            "role":role,
            "content":content
        }
    )
    
    if len(_history)>MAX_HISTORY:
        _history.pop(0)

def get_history():

    return _history.copy()

def clear_history():
    
    _history.clear()