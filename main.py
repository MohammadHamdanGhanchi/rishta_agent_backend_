from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ULTRAMSG_INSTANCE_ID = os.getenv('ULTRAMSG_INSTANCE_ID')
ULTRAMSG_TOKEN = os.getenv('ULTRAMSG_TOKEN')

class MessageRequest(BaseModel):
    phone_number: str
    message: str

@app.post('/send-message')
def send_message(data: MessageRequest):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": data.phone_number,
        "body": data.message
    }
    response = requests.post(url, data=payload)
    print("Ultramsg response:", response.text)  # Debug ke liye
    if response.status_code == 200:
        return {"success": True, "detail": "Message sent!"}
    else:
        raise HTTPException(status_code=400, detail=response.text)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 