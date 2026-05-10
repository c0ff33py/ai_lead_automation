from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import init_db, save_lead, get_all_leads
from telegram_bot import send_telegram_message

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # startup တစ်ကြိမ်ထဲ
    yield

app = FastAPI(lifespan=lifespan)

class Lead(BaseModel):
    name: str
    phone: str
    business_type: str

@app.post("/webhook/lead")
def receive_lead(lead: Lead):
    try:
        lead_id = save_lead(lead.name, lead.phone, lead.business_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    message = (
        f"🚀 New Lead #{lead_id}\n"
        f"👤 Name: {lead.name}\n"
        f"📞 Phone: {lead.phone}\n"
        f"🏢 Business: {lead.business_type}"
    )

    tg_result = send_telegram_message(message)
    tg_ok = tg_result.get("ok", False)

    return {
        "status": "success",
        "lead_id": lead_id,
        "telegram_sent": tg_ok
    }

@app.get("/leads")
def list_leads():
    return get_all_leads()

@app.get("/health")
def health():
    return {"status": "ok"}