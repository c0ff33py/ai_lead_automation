from fastapi import FastAPI  # type: ignore[reportMissingImports]
from pydantic import BaseModel  # type: ignore[reportMissingImports]
from database import save_lead
from telegram_bot import send_telegram_message

app = FastAPI()

class Lead(BaseModel):
    name: str
    phone: str
    business_type: str

@app.post("/webhook/lead")
def receive_lead(lead: Lead):

    # Save to database
    save_lead(
        lead.name,
        lead.phone,
        lead.business_type
    )

    # Send Telegram notification
    message = f"""
🚀 New Lead Received

Name: {lead.name}
Phone: {lead.phone}
Business: {lead.business_type}
"""

    send_telegram_message(message)

    return {
        "status": "success",
        "message": "Lead received"
    }