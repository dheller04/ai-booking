import openai
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

availability = {
    "2025-05-15": ["10:00 AM", "2:00 PM"],
    "2025-05-16": ["9:00 AM", "1:00 PM"]
}

class BookingRequest(BaseModel):
    message: str

@app.post("/book")
async def book_job(req: BookingRequest):
    prompt = f"""
    You are an AI assistant for a media production business. Today's date is {datetime.today().strftime('%Y-%m-%d')}.
    Available times: {json.dumps(availability)}.

    Understand the customer message below and reply with:
    - Clarify service (if needed)
    - Offer available time slots
    - Ask for confirmation to book

    Customer message: \"{req.message}\"
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return {"response": response['choices'][0]['message']['content']}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)