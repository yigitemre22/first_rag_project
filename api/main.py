from fastapi import FastAPI, Request,UploadFile,File,HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from rag.pipeline import answer_question
import shutil
from pathlib import Path
from ingestion.ingest import ingest_pdf
from database.vectore_store import get_documents,delete_document_by_filename
from memory.chat_memory import clear_history as clear_chat_history
from memory.conversation import clear_history as clear_conversation_history


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

    try:
        with open(filepath,"wb") as buffer:

            shutil.copyfileobj(file.file,buffer)

        ingest_pdf(filepath)
    
        return{
        "message":"uploaded",
        "filename":file.filename
        }
    except Exception as e:
        if filepath.exists():
            filepath.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"PDF upload failed: {str(e)}"
        )        

@app.get("/documents")
def documents():

    return{
        "documents":get_documents()
    }

@app.post("/new-chat")
def new_chat():
    clear_chat_history()
    clear_conversation_history()

    return{
        "message":"ok"
    }


@app.delete("/document/{filename}")
def delete_document(filename : str):
    delete_document_by_filename(filename)

    filepath=Path("documents")/filename

    if filepath.exists():
        filepath.unlink()

    return{
        "message":"document deleted"
    }