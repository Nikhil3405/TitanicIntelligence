from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import handle_intent

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    return handle_intent(request.question)

@app.get("/plot")
def get_plot():
    return FileResponse("output.png", media_type="image/png")