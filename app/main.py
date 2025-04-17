from fastapi import FastAPI
from app.models import ChatMessage
from app.services.chat_service import process_chat, get_thread_history

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello! I'm your AI Investment Advisor. Let's develop your investment strategy."}

# Chat endpoint
@app.post("/chat")
def chat(chat_message: ChatMessage):
    return process_chat(chat_message)

# Get thread history endpoint
@app.get("/thread/{thread_id}")
def thread_history(thread_id: str):
    return get_thread_history(thread_id) 