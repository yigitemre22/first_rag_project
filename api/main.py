from fastapi import FastAPI, Request,UploadFile,File
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from rag.pipeline import answer_question
import shutil
from pathlib import Path
from ingestion.ingest import ingest_pdf
from database.vectore_store import get_documents
from memory.chat_memory import clear_history

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    question:str
    filename:str |None=None

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.post("/chat")
def chat(data:ChatRequest):
    answer,documents=answer_question(data.question,data.filename,)

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

@app.post("/upload")
def upload_pdf(file:UploadFile=File(...)):

    documents=Path("documents")

    documents.mkdir(exist_ok=True)

    filepath=documents / file.filename

    with open(filepath,"wb") as buffer:

        shutil.copyfileobj(file.file,buffer)

    ingest_pdf(filepath)
    
    return{
        "message":"uploaded",
        "filename":file.filename
    }        

@app.get("/documents")
def documents():

    return{
        "documents":get_documents()
    }

@app.post("/new-chat")
def new_chat():
    clear_history()

    return{
        "message":"ok"
    }