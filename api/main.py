from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from rag.pipeline import answer_question

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="staticyar"
)

templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    question:str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.post("/chat")
def chat(data:ChatRequest):
    answer,documents=answer_question(data.question)

    sources=[]

    for doc in documents:
        sources.append(
            {
                "filename":doc[1],
                "page":doc[2],
                "chunk":doc[3],
                "distance":doc[5],
            }
        )
    return {
        "answer":answer,
        "sources":sources
    }